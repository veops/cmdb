# -*- coding:utf-8 -*-

from collections import defaultdict

from flask import abort

from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.models.cmdb import CI
from api.models.cmdb import CIRelation


class TreeViewManager(object):
    @classmethod
    def get(cls):
        region_type = CITypeCache.get(BuiltinModelEnum.DCIM_REGION) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_REGION))

        idc_type = CITypeCache.get(BuiltinModelEnum.DCIM_IDC) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_IDC))

        server_room_type = CITypeCache.get(BuiltinModelEnum.DCIM_SERVER_ROOM) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_SERVER_ROOM))

        rack_type = CITypeCache.get(BuiltinModelEnum.DCIM_RACK) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_RACK))

        relations = defaultdict(set)
        ids = set()
        has_parent_ids = set()

        for i in CIRelation.get_by(only_query=True).join(CI, CI.id == CIRelation.first_ci_id).filter(
                CI.type_id.in_([region_type.id, idc_type.id])):
            relations[i.first_ci_id].add(i.second_ci_id)
            ids.add(i.first_ci_id)
            ids.add(i.second_ci_id)
            has_parent_ids.add(i.second_ci_id)

        for i in CIRelation.get_by(only_query=True).join(
                CI, CI.id == CIRelation.second_ci_id).filter(CI.type_id.in_([idc_type.id, server_room_type.id])):
            relations[i.first_ci_id].add(i.second_ci_id)
            ids.add(i.first_ci_id)
            ids.add(i.second_ci_id)
            has_parent_ids.add(i.second_ci_id)

        for i in CI.get_by(only_query=True).filter(CI.type_id.in_([region_type.id, idc_type.id])):
            ids.add(i.id)

        for _id in ids:
            if _id not in has_parent_ids:
                relations[None].add(_id)

        type2name = dict()
        type2name[region_type.id] = AttributeCache.get(region_type.show_id or region_type.unique_id).name
        type2name[idc_type.id] = AttributeCache.get(idc_type.show_id or idc_type.unique_id).name
        type2name[server_room_type.id] = AttributeCache.get(server_room_type.show_id or server_room_type.unique_id).name

        response, _, _, _, _, _ = SearchFromDB(
            "_type:({})".format(";".join(map(str, [region_type.id, idc_type.id, server_room_type.id]))),
            ci_ids=list(ids),
            count=1000000,
            fl=list(type2name.values()),
            parent_node_perm_passed=True).search()
        id2ci = {i['_id']: i for i in response}

        def _build_tree(_tree, parent_id=None):
            tree = []
            for child_id in _tree.get(parent_id, []):
                children = sorted(_build_tree(_tree, child_id), key=lambda x: x['_id'])
                if not id2ci.get(child_id):
                    continue
                ci = id2ci[child_id]
                if ci['ci_type'] == BuiltinModelEnum.DCIM_SERVER_ROOM:
                    ci['rack_count'] = CIRelation.get_by(first_ci_id=child_id, only_query=True).join(
                        CI, CI.id == CIRelation.second_ci_id).filter(CI.type_id == rack_type.id).count()

                tree.append({'children': children, **ci})
            return tree

        result = sorted(_build_tree(relations), key=lambda x: x['_id'])

        return result, type2name
