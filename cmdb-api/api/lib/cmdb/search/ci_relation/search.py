# -*- coding:utf-8 -*-


import json
from collections import Counter

from flask import abort
from flask import current_app

from api.extensions import rd
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci.es.search import Search as SearchFromES
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
                 reverse=False):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort or ("ci_id" if current_app.config.get("USE_ES") else None)

        self.root_id = root_id
        self.level = level or 0
        self.reverse = reverse

    def _get_ids(self):
        merge_ids = []
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        for level in range(1, sorted(self.level)[-1] + 1):
            _tmp = list(map(lambda x: list(json.loads(x).keys()),
                            filter(lambda x: x is not None, rd.get(ids, REDIS_PREFIX_CI_RELATION) or [])))
            ids = [j for i in _tmp for j in i]
            if level in self.level:
                merge_ids.extend(ids)

        return merge_ids

    def _get_reverse_ids(self):
        merge_ids = []
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        for level in range(1, sorted(self.level)[-1] + 1):
            ids = CIRelationManager.get_ancestor_ids(ids, 1)
            if level in self.level:
                merge_ids.extend(ids)

        return merge_ids

    def search(self):
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        cis = [CI.get_by_id(_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(_id))) for _id in ids]

        merge_ids = self._get_ids() if not self.reverse else self._get_reverse_ids()

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
            type_ids = list(set(type_ids))
            if self.orig_query:
                self.orig_query = "_type:({0}),{1}".format(";".join(list(map(str, type_ids))), self.orig_query)
            else:
                self.orig_query = "_type:({0})".format(";".join(list(map(str, type_ids))))

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
        _tmp = []
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        for lv in range(0, self.level):
            if not lv:
                if type_ids and lv == self.level - 1:
                    _tmp = list(map(lambda x: [i for i in x if i[1] in type_ids],
                                    (map(lambda x: list(json.loads(x).items()),
                                         [i or '{}' for i in rd.get(ids, REDIS_PREFIX_CI_RELATION) or []]))))
                else:
                    _tmp = list(map(lambda x: list(json.loads(x).items()),
                                    [i or '{}' for i in rd.get(ids, REDIS_PREFIX_CI_RELATION) or []]))
            else:
                for idx, item in enumerate(_tmp):
                    if item:
                        if type_ids and lv == self.level - 1:
                            __tmp = list(
                                map(lambda x: [(_id, type_id) for _id, type_id in json.loads(x).items()
                                               if type_id in type_ids],
                                    filter(lambda x: x is not None,
                                           rd.get([i[0] for i in item], REDIS_PREFIX_CI_RELATION) or [])))
                        else:

                            __tmp = list(map(lambda x: list(json.loads(x).items()),
                                             filter(lambda x: x is not None,
                                                    rd.get([i[0] for i in item], REDIS_PREFIX_CI_RELATION) or [])))

                        _tmp[idx] = [j for i in __tmp for j in i]
                    else:
                        _tmp[idx] = []

        result = {str(_id): len(_tmp[idx]) for idx, _id in enumerate(ids)}

        result.update(
            detail={str(_id): dict(Counter([i[1] for i in _tmp[idx]]).items()) for idx, _id in enumerate(ids)})

        return result
