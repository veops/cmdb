# -*- coding:utf-8 -*-


from __future__ import unicode_literals

from flask import current_app

from api.extensions import es
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import RetKey
from api.lib.utils import handle_arg_list
from api.models.cmdb import Attribute


class SearchError(Exception):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return self.v


class Search(object):
    def __init__(self, query=None, fl=None, facet_field=None, page=1, ret_key=RetKey.NAME, count=1, sort=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.ret_key = ret_key
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort

        self.query = dict(filter=dict(bool=dict(should=[], must=[], must_not=[])))

    @staticmethod
    def _operator_proc(key):
        operator = "&"
        if key.startswith("+"):
            key = key[1:].strip()
        elif key.startswith("-"):
            operator = "|"
            key = key[1:].strip()
        elif key.startswith("~"):
            operator = "~"
            key = key[1:].strip()

        return operator, key

    def _operator2query(self, operator):
        if operator == "&":
            return self.query['query']['bool']['must']
        elif operator == "|":
            return self.query['query']['bool']['should']
        else:
            return self.query['query']['bool']['must_not']

    def _attr_name_proc(self, key):
        operator, key = self._operator_proc(key)

        if key in ('ci_type', 'type', '_type'):
            return 'ci_type', Attribute.TEXT, operator

        if key in ('id', 'ci_id', '_id'):
            return 'ci_id', Attribute.TEXT, operator

        attr = AttributeCache.get(key)
        if attr:
            return attr.name, attr.value_type, operator
        else:
            raise SearchError("{0} is not existed".format(key))

    def _in_query_handle(self, attr, v):
        terms = v[1:-1].split(";")
        operator = "|"
        for term in terms:
            self._operator2query(operator).append({
                "term": {
                    attr: term
                }
            })

    @staticmethod
    def _digit(s):
        if s.isdigit():
            return int(float(s))
        return s

    def _range_query_handle(self, attr, v, operator):
        left, right = v.split("_TO_")
        left, right = left.strip()[1:], right.strip()[:-1]
        self._operator2query(operator).append({
            "range": {
                attr: {
                    "to": self._digit(right),
                    "from": self._digit(left),
                }
            }
        })

    def _comparison_query_handle(self, attr, v, operator):
        if v.startswith(">="):
            _query = dict(gte=self._digit(v[2:]))
        elif v.startswith("<="):
            _query = dict(lte=self._digit(v[2:]))
        elif v.startswith(">"):
            _query = dict(gt=self._digit(v[1:]))
        elif v.startswith("<"):
            _query = dict(lt=self._digit(v[1:]))
        else:
            return

        self._operator2query(operator).append({
            "range": {
                attr: _query
            }
        })

    def _match_query_handle(self, attr, v, operator):
        if "*" in v:
            self._operator2query(operator).append({
                "wildcard": {
                    attr: v
                }
            })
        else:
            self._operator2query(operator).append({
                "term": {
                    attr: v
                }
            })

    def __query_build_by_field(self, queries):

        for q in queries:
            if ":" in q:
                k = q.split(":")[0].strip()
                v = ":".join(q.split(":")[1:]).strip()
                field_name, field_type, operator = self._attr_name_proc(k)
                if field_name:
                    # in query
                    if v.startswith("(") and v.endswith(")"):
                        self._in_query_handle(field_name, v)
                    # range query
                    elif v.startswith("[") and v.endswith("]") and "_TO_" in v:
                        self._range_query_handle(field_name, v, operator)
                    # comparison query
                    elif v.startswith(">=") or v.startswith("<=") or v.startswith(">") or v.startswith("<"):
                        self._comparison_query_handle(field_name, v, operator)
                    else:
                        self._match_query_handle(field_name, v, operator)
                else:
                    raise SearchError("argument q format invalid: {0}".format(q))
            elif q:
                raise SearchError("argument q format invalid: {0}".format(q))

    def _query_build_raw(self):

        queries = handle_arg_list(self.orig_query)
        current_app.logger.debug(queries)

        self.__query_build_by_field(queries)

        self._paginate_build()

        filter_path = self._fl_build()

        sort = self._sort_build()

        return es.read(self.query, filter_path=filter_path, sort=sort)

    def _facet_build(self):
        return {
            "aggs": {
                self.facet_field: {
                    "cardinality": {
                        "field": self.facet_field
                    }
                }
            }
        }

    def _sort_build(self):
        fields = list(filter(lambda x: x != "", self.sort or ""))
        sorts = []
        for field in fields:
            sort_type = "asc"
            if field.startswith("+"):
                field = field[1:]
            elif field.startswith("-"):
                field = field[1:]
                sort_type = "desc"
            else:
                continue
            sorts.append({field: {"order": sort_type}})

        return sorts

    def _paginate_build(self):
        self.query.update({"from": (self.page - 1) * self.count,
                           "size": self.count})

    def _fl_build(self):
        return ['hits.hits._source.{0}'.format(i) for i in self.fl]

    def search(self):
        try:
            numfound, cis = self._query_build_raw()
        except Exception as e:
            current_app.logger.error(str(e))
            raise SearchError("unknown search error")

        if self.facet_field and numfound:
            facet = self._facet_build()
        else:
            facet = dict()

        total = len(cis)

        return cis, {}, total, self.page, numfound, facet
