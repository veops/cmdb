# -*- coding:utf-8 -*-

__all__ = ['db', 'es', 'search']

from flask import current_app

from api.lib.cmdb.const import RetKey
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci.es.search import Search as SearchFromES


def search(query=None,
           fl=None,
           facet=None,
           page=1,
           ret_key=RetKey.NAME,
           count=1,
           sort=None,
           excludes=None,
           use_id_filter=True):
    if current_app.config.get("USE_ES"):
        s = SearchFromES(query, fl, facet, page, ret_key, count, sort)
    else:
        s = SearchFromDB(query, fl, facet, page, ret_key, count, sort, excludes=excludes, use_id_filter=use_id_filter)

    return s
