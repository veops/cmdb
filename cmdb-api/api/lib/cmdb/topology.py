# -*- coding:utf-8 -*-

import json

from flask import abort

from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci import search
from api.models.cmdb import TopologyView
from api.models.cmdb import TopologyViewGroup


class TopologyViewManager(object):
    group_cls = TopologyViewGroup
    cls = TopologyView

    def get_view_by_id(self, _id):
        res = self.cls.get_by_id(_id)

        return res and res.to_dict() or {}

    @classmethod
    def add_group(cls, name, order):
        if order is None:
            cur_max_order = cls.group_cls.get_by(only_query=True).order_by(cls.group_cls.order.desc()).first()
            cur_max_order = cur_max_order and cur_max_order.order or 0
            order = cur_max_order + 1

        cls.group_cls.get_by(name=name, first=True, to_dict=False) and abort(
            400, ErrFormat.topology_group_exists.format(name))

        return cls.group_cls.create(name=name, order=order)

    def update_group(self, group_id, name, view_ids):
        existed = self.group_cls.get_by_id(group_id) or abort(404, ErrFormat.not_found)
        if name is not None and name != existed.name:
            existed.update(name=name)

        for idx, view_id in enumerate(view_ids):
            view = self.cls.get_by_id(view_id)
            if view is not None:
                view.update(group_id=group_id, order=idx)

        return existed.to_dict()

    @classmethod
    def delete_group(cls, _id):
        existed = cls.group_cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        for item in cls.cls.get_by(group_id=_id, to_dict=False):
            item.update(group_id=None, filter_none=False)

        existed.soft_delete()

    @classmethod
    def group_order(cls, group_ids):
        for idx, group_id in enumerate(group_ids):
            group = cls.group_cls.get_by_id(group_id)
            group.update(order=idx + 1)

    @classmethod
    def add(cls, name, group_id, option, order=None, **kwargs):
        cls.cls.get_by(name=name, first=True) and abort(400, ErrFormat.topology_exists.format(name))
        if order is None:
            cur_max_order = cls.cls.get_by(group_id=group_id, only_query=True).order_by(
                cls.cls.order.desc()).first()
            cur_max_order = cur_max_order and cur_max_order.order or 0
            order = cur_max_order + 1

        return cls.cls.create(name=name, group_id=group_id, option=option, order=order, **kwargs).to_dict()

    @classmethod
    def update(cls, _id, **kwargs):
        existed = cls.cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        return existed.update(filter_none=False, **kwargs).to_dict()

    @classmethod
    def delete(cls, _id):
        existed = cls.cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        existed.soft_delete()

    @classmethod
    def group_inner_order(cls, _ids):
        for idx, _id in enumerate(_ids):
            topology = cls.cls.get_by_id(_id)
            topology.update(order=idx + 1)

    @classmethod
    def get_all(cls):
        groups = cls.group_cls.get_by(to_dict=True)
        groups = sorted(groups, key=lambda x: x['order'])
        group2pos = {group['id']: idx for idx, group in enumerate(groups)}

        topo_views = sorted(cls.cls.get_by(to_dict=True), key=lambda x: x['order'])
        other_group = dict(views=[])
        for view in topo_views:
            if view['group_id']:
                groups[group2pos[view['group_id']]].setdefault('views', []).append(view)
            else:
                other_group['views'].append(view)

        if other_group['views']:
            groups.append(other_group)

        return groups

    @staticmethod
    def relation_from_ci_type(type_id):
        nodes, edges = CITypeRelationManager.get_relations_by_type_id(type_id)

        return dict(nodes=nodes, edges=edges)

    def topology_view(self, view_id):
        view = self.cls.get_by_id(view_id) or abort(404, ErrFormat.not_found)
        nodes, links = [], []

        _type = CITypeCache.get(view.central_node_type)
        if not _type:
            return {}
        root_ids = []
        show_key = AttributeCache.get(_type.show_id or _type.unique_id)

        q = (view.central_node_instances[2:] if view.central_node_instances.startswith('q=') else
             view.central_node_instances)
        s = search(q, fl=['_id', show_key.name], count=1000000)
        try:
            response, _, _, _, _, _ = s.search()
        except SearchError:
            return {}
        for i in response:
            root_ids.append(i['_id'])
            nodes.append(dict(id=i['_id'], name=i[show_key.name]))

        prefix = REDIS_PREFIX_CI_RELATION
        key = list(map(str, root_ids))
        id2node = {}
        for level in sorted([i for i in view.path.keys() if int(i) > 0]):
            type_ids = {int(i) for i in view.path[level]}

            res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(key, prefix) or []]]
            new_key = []
            for idx, from_id in enumerate(key):
                for to_id, type_id in res[idx]:
                    if type_id in type_ids:
                        links.append({'from': from_id, 'to': to_id})
                        id2node[to_id] = {'id': to_id, 'type_id': type_id}
                        new_key.append(to_id)

            key = new_key

        ci_ids = list(map(int, root_ids))
        for level in sorted([i for i in view.path.keys() if int(i) < 0], reverse=True):
            type_ids = {int(i) for i in view.path[level]}

            res = CIRelationManager.get_parent_ids(ci_ids)
            _ci_ids = []
            for from_id in res:
                for to_id, type_id in res[from_id]:
                    if type_id in type_ids:
                        from_id, to_id = str(from_id), str(to_id)
                        links.append({'from': from_id, 'to': to_id})
                        id2node[to_id] = {'id': str(to_id), 'type_id': type_id}
                        _ci_ids.append(to_id)

            ci_ids = _ci_ids

        fl = set()
        type_ids = {t for lv in view.path if lv != '0' for t in view.path[lv]}
        type2show = {}
        for type_id in type_ids:
            ci_type = CITypeCache.get(type_id)
            if ci_type:
                attr = AttributeCache.get(ci_type.show_id or ci_type.unique_id)
                if attr:
                    fl.add(attr.name)
                    type2show[type_id] = attr.name
        s = search("_id:({})".format(';'.join(id2node.keys())), fl=list(fl), count=1000000)
        try:
            response, _, _, _, _, _ = s.search()
        except SearchError:
            return {}
        for i in response:
            id2node[str(i['_id'])]['name'] = i[type2show[str(i['_type'])]]
        nodes.extend(id2node.values())

        return dict(nodes=nodes, links=links)
