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
    def __init__(self, root_id, level=1, query=None, fl=None, facet_field=None, page=1, count=None, sort=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort or ("ci_id" if current_app.config.get("USE_ES") else None)

        self.root_id = root_id
        self.level = int(level)

    def search(self):
        ci = CI.get_by_id(self.root_id) or abort(404, "CI <{0}> does not exist".format(self.root_id))
        ids = [self.root_id]
        for _ in range(0, self.level):
            _tmp = list(map(json.loads, filter(lambda x: x is not None, rd.get(ids, REDIS_PREFIX_CI_RELATION))))
            ids = [j for i in _tmp for j in i]
        if not self.orig_query or ("_type:" not in self.orig_query
                                   and "type_id:" not in self.orig_query
                                   and "ci_type:" not in self.orig_query):
            type_ids = CITypeRelationManager.get_child_type_ids(ci.type_id, self.level)
            self.orig_query = "_type:({0}),{1}".format(";".join(list(map(str, type_ids))), self.orig_query)

        if current_app.config.get("USE_ES"):
            return SearchFromES(self.orig_query,
                                fl=self.fl,
                                facet_field=self.facet_field,
                                page=self.page,
                                count=self.count,
                                sort=self.sort,
                                ci_ids=ids).search()
        else:
            return SearchFromDB(self.orig_query,
                                fl=self.fl,
                                facet_field=self.facet_field,
                                page=self.page,
                                count=self.count,
                                sort=self.sort,
                                ci_ids=ids).search()
