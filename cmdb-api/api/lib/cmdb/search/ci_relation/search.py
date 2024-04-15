# -*- coding:utf-8 -*-
import json
import sys
from collections import Counter

from flask import abort
from flask import current_app
from flask_login import current_user

from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION2
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci.es.search import Search as SearchFromES
from api.lib.cmdb.utils import TableMap
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.models.cmdb import CI


class Search(object):
    def __init__(self, root_id,
                 level=None,
                 query=None,
                 fl=None,
                 facet_field=None,
                 page=1,
                 count=None,
                 sort=None,
                 reverse=False,
                 ancestor_ids=None,
                 descendant_ids=None,
                 has_m2m=None,
                 root_parent_path=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort or ("ci_id" if current_app.config.get("USE_ES") else None)

        self.root_id = root_id
        self.level = level or 0
        self.reverse = reverse

        self.level2constraint = CITypeRelationManager.get_level2constraint(
            root_id[0] if root_id and isinstance(root_id, list) else root_id,
            level[0] if isinstance(level, list) and level else level)

        self.ancestor_ids = ancestor_ids
        self.descendant_ids = descendant_ids
        self.root_parent_path = root_parent_path
        self.has_m2m = has_m2m or False
        if not self.has_m2m:
            if self.ancestor_ids:
                self.has_m2m = True
            else:
                level = level[0] if isinstance(level, list) and level else level
                for _l, c in self.level2constraint.items():
                    if _l < int(level) and c == ConstraintEnum.Many2Many:
                        self.has_m2m = True

        self.type2filter_perms = None

        self.is_app_admin = is_app_admin('cmdb') or current_user.username == "worker"

    def _get_ids(self, ids):

        merge_ids = []
        key = []
        _tmp = []
        for level in range(1, sorted(self.level)[-1] + 1):
            if len(self.descendant_ids) >= level and self.type2filter_perms.get(self.descendant_ids[level - 1]):
                id_filter_limit, _ = self._get_ci_filter(self.type2filter_perms[self.descendant_ids[level - 1]])
            else:
                id_filter_limit = {}

            if not self.has_m2m:
                key, prefix = list(map(str, ids)), REDIS_PREFIX_CI_RELATION

            else:
                if not self.ancestor_ids:
                    if level == 1:
                        key, prefix = list(map(str, ids)), REDIS_PREFIX_CI_RELATION
                    else:
                        key = list(set(["{},{}".format(i, j) for idx, i in enumerate(key) for j in _tmp[idx]]))
                        prefix = REDIS_PREFIX_CI_RELATION2
                else:
                    if level == 1:
                        key, prefix = ["{},{}".format(self.ancestor_ids, i) for i in ids], REDIS_PREFIX_CI_RELATION2
                    else:
                        key = list(set(["{},{}".format(i, j) for idx, i in enumerate(key) for j in _tmp[idx]]))
                        prefix = REDIS_PREFIX_CI_RELATION2

            if not key or id_filter_limit is None:
                return []

            res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(key, prefix) or []]]
            _tmp = [[i[0] for i in x if (not id_filter_limit or (
                    key[idx] not in id_filter_limit or int(i[0]) in id_filter_limit[key[idx]]) or
                                         int(i[0]) in id_filter_limit)] for idx, x in enumerate(res)]

            ids = [j for i in _tmp for j in i]

            if level in self.level:
                merge_ids.extend(ids)

        return merge_ids

    def _get_reverse_ids(self, ids):
        merge_ids = []
        level2ids = {}
        for level in range(1, sorted(self.level)[-1] + 1):
            ids, _level2ids = CIRelationManager.get_ancestor_ids(ids, 1)

            if _level2ids.get(2):
                level2ids[level + 1] = _level2ids[2]

            if level in self.level:
                if level in level2ids and level2ids[level]:
                    merge_ids.extend(set(ids) & set(level2ids[level]))
                else:
                    merge_ids.extend(ids)

        return merge_ids

    def _has_read_perm_from_parent_nodes(self):
        self.root_parent_path = list(map(str, self.root_parent_path))
        if str(self.root_id).isdigit() and str(self.root_id) not in self.root_parent_path:
            self.root_parent_path.append(str(self.root_id))
        self.root_parent_path = set(self.root_parent_path)

        if self.is_app_admin:
            self.type2filter_perms = {}
            return True

        res = ACLManager().get_resources(ResourceTypeEnum.CI_FILTER) or {}
        self.type2filter_perms = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res]))) or {}
        for _, filters in self.type2filter_perms.items():
            if set((filters.get('id_filter') or {}).keys()) & self.root_parent_path:
                return True

        return True

    def search(self):
        use_ci_filter = len(self.descendant_ids) == self.level[0] - 1
        parent_node_perm_passed = self._has_read_perm_from_parent_nodes()

        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        cis = [CI.get_by_id(_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(_id))) for _id in ids]

        merge_ids = self._get_ids(ids) if not self.reverse else self._get_reverse_ids(ids)

        if not self.orig_query or ("_type:" not in self.orig_query
                                   and "type_id:" not in self.orig_query
                                   and "ci_type:" not in self.orig_query):
            type_ids = []
            for level in self.level:
                for ci in cis:
                    if not self.reverse:
                        type_ids.extend(CITypeRelationManager.get_child_type_ids(ci.type_id, level))
                    else:
                        type_ids.extend(CITypeRelationManager.get_parent_type_ids(ci.type_id, level))
            type_ids = set(type_ids)
            if self.orig_query:
                self.orig_query = "_type:({0}),{1}".format(";".join(map(str, type_ids)), self.orig_query)
            else:
                self.orig_query = "_type:({0})".format(";".join(map(str, type_ids)))

        if not merge_ids:
            # cis, counter, total, self.page, numfound, facet_
            return [], {}, 0, self.page, 0, {}

        if current_app.config.get("USE_ES"):
            return SearchFromES(self.orig_query,
                                fl=self.fl,
                                facet_field=self.facet_field,
                                page=self.page,
                                count=self.count,
                                sort=self.sort,
                                ci_ids=merge_ids).search()
        else:
            return SearchFromDB(self.orig_query,
                                fl=self.fl,
                                facet_field=self.facet_field,
                                page=self.page,
                                count=self.count,
                                sort=self.sort,
                                ci_ids=merge_ids,
                                parent_node_perm_passed=parent_node_perm_passed,
                                use_ci_filter=use_ci_filter).search()

    def _get_ci_filter(self, filter_perms, ci_filters=None):
        ci_filters = ci_filters or []
        if ci_filters:
            result = {}
            for item in ci_filters:
                res = SearchFromDB('_type:{},{}'.format(item['type_id'], item['ci_filter']),
                                   count=sys.maxsize, parent_node_perm_passed=True).get_ci_ids()
                if res:
                    result[item['type_id']] = set(res)

            return {}, result if result else None

        result = dict()
        if filter_perms.get('id_filter'):
            for k in filter_perms['id_filter']:
                node_path = k.split(',')
                if len(node_path) == 1:
                    result[int(node_path[0])] = 1
                elif not self.has_m2m:
                    result.setdefault(node_path[-2], set()).add(int(node_path[-1]))
                else:
                    result.setdefault(','.join(node_path[:-1]), set()).add(int(node_path[-1]))
            if result:
                return result, None
            else:
                return None, None

        return {}, None

    def statistics(self, type_ids, need_filter=True):
        self.level = int(self.level)

        acl = ACLManager('cmdb')

        type2filter_perms = dict()
        if not self.is_app_admin:
            res2 = acl.get_resources(ResourceTypeEnum.CI_FILTER)
            if res2:
                type2filter_perms = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res2])))

        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        _tmp, tmp_res = [], []
        level2ids = {}
        for lv in range(1, self.level + 1):
            level2ids[lv] = []

            if need_filter:
                id_filter_limit, ci_filter_limit = None, None
                if len(self.descendant_ids or []) >= lv and type2filter_perms.get(self.descendant_ids[lv - 1]):
                    id_filter_limit, _ = self._get_ci_filter(type2filter_perms[self.descendant_ids[lv - 1]])
                elif type_ids and self.level == lv:
                    ci_filters = [type2filter_perms[type_id] for type_id in type_ids if type_id in type2filter_perms]
                    if ci_filters:
                        id_filter_limit, ci_filter_limit = self._get_ci_filter({}, ci_filters=ci_filters)
                    else:
                        id_filter_limit = {}
                else:
                    id_filter_limit = {}
            else:
                id_filter_limit, ci_filter_limit = {}, {}

            if lv == 1:
                if not self.has_m2m:
                    key, prefix = [str(i) for i in ids], REDIS_PREFIX_CI_RELATION
                else:
                    key = ["{},{}".format(self.ancestor_ids, _id) for _id in ids]
                    if not self.ancestor_ids:
                        key, prefix = [str(i) for i in ids], REDIS_PREFIX_CI_RELATION
                    else:
                        prefix = REDIS_PREFIX_CI_RELATION2

                    level2ids[lv] = [[i] for i in key]

                if not key or id_filter_limit is None:
                    _tmp = [[]] * len(ids)
                    continue

                res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(key, prefix) or []]]
                _tmp = []
                if type_ids and lv == self.level:
                    _tmp = [[i for i in x if i[1] in type_ids and
                             (not id_filter_limit or (key[idx] not in id_filter_limit or
                                                      int(i[0]) in id_filter_limit[key[idx]]) or
                              int(i[0]) in id_filter_limit)] for idx, x in enumerate(res)]
                else:
                    _tmp = [[i for i in x if (not id_filter_limit or (key[idx] not in id_filter_limit or
                                                                      int(i[0]) in id_filter_limit[key[idx]]) or
                                              int(i[0]) in id_filter_limit)] for idx, x in enumerate(res)]

                if ci_filter_limit:
                    _tmp = [[j for j in i if j[1] not in ci_filter_limit or int(j[0]) in ci_filter_limit[j[1]]]
                            for i in _tmp]

            else:

                for idx, item in enumerate(_tmp):
                    if item:
                        if not self.has_m2m:
                            key, prefix = [i[0] for i in item], REDIS_PREFIX_CI_RELATION
                        else:
                            key = list(set(['{},{}'.format(j, i[0]) for i in item for j in level2ids[lv - 1][idx]]))
                            prefix = REDIS_PREFIX_CI_RELATION2

                            level2ids[lv].append(key)

                        if key:
                            res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(key, prefix) or []]]
                            if type_ids and lv == self.level:
                                tmp_res = [[i for i in x if i[1] in type_ids and
                                            (not id_filter_limit or (
                                                    key[idx] not in id_filter_limit or
                                                    int(i[0]) in id_filter_limit[key[idx]]) or
                                             int(i[0]) in id_filter_limit)] for idx, x in enumerate(res)]
                            else:
                                tmp_res = [[i for i in x if (not id_filter_limit or (
                                        key[idx] not in id_filter_limit or
                                        int(i[0]) in id_filter_limit[key[idx]]) or
                                                             int(i[0]) in id_filter_limit)] for idx, x in
                                           enumerate(res)]

                            if ci_filter_limit:
                                tmp_res = [[j for j in i if j[1] not in ci_filter_limit or
                                            int(j[0]) in ci_filter_limit[j[1]]] for i in tmp_res]
                        else:
                            tmp_res = []

                        if tmp_res:
                            _tmp[idx] = [j for i in tmp_res for j in i]
                    else:
                        _tmp[idx] = []
                        level2ids[lv].append([])

        result = {str(_id): len(_tmp[idx]) for idx, _id in enumerate(ids)}

        result.update(
            detail={str(_id): dict(Counter([i[1] for i in _tmp[idx]]).items()) for idx, _id in enumerate(ids)})

        return result

    def search_full(self, type_ids):
        def _get_id2name(_type_id):
            ci_type = CITypeCache.get(_type_id)
            attr = AttributeCache.get(ci_type.show_id) or AttributeCache.get(ci_type.unique_id)
            value_table = TableMap(attr=attr).table

            return {i.ci_id: i.value for i in value_table.get_by(attr_id=attr.id, to_dict=False)}

        self.level = int(self.level)

        acl = ACLManager('cmdb')

        type2filter_perms = dict()
        if not self.is_app_admin:
            res2 = acl.get_resources(ResourceTypeEnum.CI_FILTER)
            if res2:
                type2filter_perms = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res2])))

        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id

        level_ids = [str(i) for i in ids]
        result = []
        id2children = {}
        id2name = _get_id2name(type_ids[0])
        for i in level_ids:
            item = dict(id=int(i),
                        type_id=type_ids[0],
                        isLeaf=False,
                        title=id2name.get(int(i)),
                        children=[])
            result.append(item)
            id2children[str(i)] = item['children']

        for lv in range(1, self.level):

            if len(type_ids or []) >= lv and type2filter_perms.get(type_ids[lv]):
                id_filter_limit, _ = self._get_ci_filter(type2filter_perms[type_ids[lv]])
            else:
                id_filter_limit = {}

            if self.has_m2m and lv != 1:
                key, prefix = [i for i in level_ids], REDIS_PREFIX_CI_RELATION2
            else:
                key, prefix = [i.split(',')[-1] for i in level_ids], REDIS_PREFIX_CI_RELATION

            res = [json.loads(x).items() for x in [i or '{}' for i in rd.get(key, prefix) or []]]
            res = [[i for i in x if (not id_filter_limit or (key[idx] not in id_filter_limit or
                                                             int(i[0]) in id_filter_limit[key[idx]]) or
                                     int(i[0]) in id_filter_limit)] for idx, x in enumerate(res)]

            _level_ids = []
            type_id = type_ids[lv]
            id2name = _get_id2name(type_id)
            for idx, _id in enumerate(level_ids):
                for child_id, _ in (res[idx] or []):
                    item = dict(id=int(child_id),
                                type_id=type_id,
                                isLeaf=True if lv == self.level - 1 else False,
                                title=id2name.get(int(child_id)),
                                children=[])
                    id2children[_id.split(',')[-1]].append(item)
                    id2children[child_id] = item['children']
                    _level_ids.append("{},{}".format(_id, child_id))

            level_ids = _level_ids

        return result
