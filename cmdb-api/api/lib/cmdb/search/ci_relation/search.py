# -*- coding:utf-8 -*-


import json

from flask import abort
from flask import current_app

from api.extensions import rd
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
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
                 sort=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort or ("ci_id" if current_app.config.get("USE_ES") else None)

        self.root_id = root_id
        self.level = level

    def search(self):
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        cis = [CI.get_by_id(_id) or abort(404, "CI <{0}> does not exist".format(_id)) for _id in ids]

        merge_ids = []
        for level in self.level:
            ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
            for _ in range(0, level):
                _tmp = list(map(lambda x: list(json.loads(x).keys()),
                                filter(lambda x: x is not None, rd.get(ids, REDIS_PREFIX_CI_RELATION) or [])))
                ids = [j for i in _tmp for j in i]

            merge_ids.extend(ids)

        if not self.orig_query or ("_type:" not in self.orig_query
                                   and "type_id:" not in self.orig_query
                                   and "ci_type:" not in self.orig_query):
            type_ids = []
            for level in self.level:
                for ci in cis:
                    type_ids.extend(CITypeRelationManager.get_child_type_ids(ci.type_id, level))
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
        _tmp = []
        ids = [self.root_id] if not isinstance(self.root_id, list) else self.root_id
        for l in range(0, int(self.level)):
            if not l:
                _tmp = list(map(lambda x: list(json.loads(x).keys()),
                                [i or '{}' for i in rd.get(ids, REDIS_PREFIX_CI_RELATION) or []]))
            else:
                for idx, i in enumerate(_tmp):
                    if i:
                        if type_ids and l == self.level - 1:
                            __tmp = list(
                                map(lambda x: list({_id: 1 for _id, type_id in json.loads(x).items()
                                                    if type_id in type_ids}.keys()),
                                    filter(lambda x: x is not None,
                                           rd.get(i, REDIS_PREFIX_CI_RELATION) or [])))
                        else:

                            __tmp = list(map(lambda x: list(json.loads(x).keys()),
                                             filter(lambda x: x is not None,
                                                    rd.get(i, REDIS_PREFIX_CI_RELATION) or [])))
                        _tmp[idx] = [j for i in __tmp for j in i]
                    else:
                        _tmp[idx] = []

        return {_id: len(_tmp[idx]) for idx, _id in enumerate(ids)}
