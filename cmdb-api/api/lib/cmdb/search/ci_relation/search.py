# -*- coding:utf-8 -*-
import json
from collections import Counter

from flask import abort
from flask import current_app

from api.extensions import rd
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION2
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci.es.search import Search as SearchFromES
from api.models.cmdb import CI
from api.models.cmdb import CIRelation


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
                 ancestor_ids=None):
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
        self.has_m2m = False
        if self.ancestor_ids:
            self.has_m2m = True
        else:
            level = level[0] if isinstance(level, list) and level else level
            for _l, c in self.level2constraint.items():
                if _l < int(level) and c == ConstraintEnum.Many2Many:
                    self.has_m2m = True

    def _get_ids(self, ids):
        if self.level[-1] == 1 and len(ids) == 1:
            if self.ancestor_ids is None:
                return [i.second_ci_id for i in CIRelation.get_by(first_ci_id=ids[0], to_dict=False)]

            else:
                seconds = {i.second_ci_id for i in CIRelation.get_by(first_ci_id=ids[0],
                                                                     ancestor_ids=self.ancestor_ids,
                                                                     to_dict=False)}

                return list(seconds)

        merge_ids = []
        key = []
        _tmp = []
        for level in range(1, sorted(self.level)[-1] + 1):
            if not self.has_m2m:
                _tmp = map(lambda x: json.loads(x).keys(),
                           filter(lambda x: x is not None, rd.get(ids, REDIS_PREFIX_CI_RELATION) or []))
                ids = [j for i in _tmp for j in i]
                key, prefix = ids, REDIS_PREFIX_CI_RELATION

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

            if not key:
                return []

            _tmp = list(map(lambda x: json.loads(x).keys() if x else [], rd.get(key, prefix) or []))
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

    def search(self):
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
                                ci_ids=merge_ids).search()

    def statistics(self, type_ids):
        self.level = int(self.level)

        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        _tmp = []
        level2ids = {}
        for lv in range(1, self.level + 1):
            level2ids[lv] = []

            if lv == 1:
                if not self.has_m2m:
                    key, prefix = ids, REDIS_PREFIX_CI_RELATION
                else:
                    if not self.ancestor_ids:
                        key, prefix = ids, REDIS_PREFIX_CI_RELATION
                    else:
                        key = ["{},{}".format(self.ancestor_ids, _id) for _id in ids]
                        prefix = REDIS_PREFIX_CI_RELATION2

                    level2ids[lv] = [[i] for i in key]

                if not key:
                    _tmp = []
                    continue

                if type_ids and lv == self.level:
                    _tmp = list(map(lambda x: [i for i in x if i[1] in type_ids],
                                    (map(lambda x: list(json.loads(x).items()),
                                         [i or '{}' for i in rd.get(key, prefix) or []]))))
                else:
                    _tmp = list(map(lambda x: list(json.loads(x).items()),
                                    [i or '{}' for i in rd.get(key, prefix) or []]))

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
                            if type_ids and lv == self.level:
                                __tmp = map(lambda x: [(_id, type_id) for _id, type_id in json.loads(x).items()
                                                       if type_id in type_ids],
                                            filter(lambda x: x is not None,
                                                   rd.get(key, prefix) or []))
                            else:
                                __tmp = map(lambda x: list(json.loads(x).items()),
                                            filter(lambda x: x is not None,
                                                   rd.get(key, prefix) or []))
                        else:
                            __tmp = []

                        _tmp[idx] = [j for i in __tmp for j in i]
                    else:
                        _tmp[idx] = []
                        level2ids[lv].append([])

        result = {str(_id): len(_tmp[idx]) for idx, _id in enumerate(ids)}

        result.update(
            detail={str(_id): dict(Counter([i[1] for i in _tmp[idx]]).items()) for idx, _id in enumerate(ids)})

        return result
