# -*- coding:utf-8 -*-


from __future__ import unicode_literals

import six
from flask import current_app

from api.extensions import es
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.search import SearchError
from api.lib.utils import handle_arg_list


class Search(object):
    def __init__(self, query=None,
                 fl=None,
                 facet_field=None,
                 page=1,
                 ret_key=RetKey.NAME,
                 count=1,
                 sort=None,
                 ci_ids=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.ret_key = ret_key
        self.count = count or current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort or "ci_id"
        self.ci_ids = ci_ids or []

        self.query = dict(query=dict(bool=dict(should=[], must=[], must_not=[])))

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
            return 'ci_type', ValueTypeEnum.TEXT, operator

        if key in ('id', 'ci_id', '_id'):
            return 'ci_id', ValueTypeEnum.TEXT, operator

        attr = AttributeCache.get(key)
        if attr:
            return attr.name, attr.value_type, operator
        else:
            raise SearchError("{0} is not existed".format(key))

    def _in_query_handle(self, attr, v):
        terms = v[1:-1].split(";")
        operator = "|"
        if attr in ('_type', 'ci_type', 'type_id') and terms and terms[0].isdigit():
            attr = "type_id"
            terms = map(int, terms)
        current_app.logger.warning(terms)
        for term in terms:
            self._operator2query(operator).append({
                "term": {
                    attr: term
                }
            })

    def _filter_ids(self):
        if self.ci_ids:
            self.query['query']['bool'].update(dict(filter=dict(terms=dict(ci_id=self.ci_ids))))

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
                    "lte": self._digit(right),
                    "gte": self._digit(left),
                    "boost": 2.0
                }
            }
        })

    def _comparison_query_handle(self, attr, v, operator):
        if v.startswith(">="):
            _query = dict(gte=self._digit(v[2:]), boost=2.0)
        elif v.startswith("<="):
            _query = dict(lte=self._digit(v[2:]), boost=2.0)
        elif v.startswith(">"):
            _query = dict(gt=self._digit(v[1:]), boost=2.0)
        elif v.startswith("<"):
            _query = dict(lt=self._digit(v[1:]), boost=2.0)
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
                    attr: v.lower() if isinstance(v, six.string_types) else v
                }
            })
        else:
            if attr == "ci_type" and v.isdigit():
                attr = "type_id"
            self._operator2query(operator).append({
                "term": {
                    attr: v.lower() if isinstance(v, six.string_types) else v
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

        self._sort_build()

        self._facet_build()

        self._filter_ids()

        return es.read(self.query, filter_path=filter_path)

    def _facet_build(self):
        aggregations = dict(aggs={})
        for field in self.facet_field:
            attr = AttributeCache.get(field)
            if not attr:
                raise SearchError("Facet by <{0}> does not exist".format(field))
            aggregations['aggs'].update({
                field: {
                    "terms": {
                        "field": "{0}.keyword".format(field)
                        if attr.value_type not in (ValueTypeEnum.INT, ValueTypeEnum.FLOAT) else field
                    }
                }
            })

        if aggregations['aggs']:
            self.query.update(aggregations)

    def _sort_build(self):
        fields = list(filter(lambda x: x != "", (self.sort or "").split(",")))
        sorts = []
        for field in fields:
            sort_type = "asc"
            if field.startswith("+"):
                field = field[1:]
            elif field.startswith("-"):
                field = field[1:]
                sort_type = "desc"
            else:
                field = field
            if field == "ci_id":
                sorts.append({field: {"order": sort_type}})
                continue

            attr = AttributeCache.get(field)
            if not attr:
                raise SearchError("Sort by <{0}> does not exist".format(field))

            sort_by = "{0}.keyword".format(field) \
                if attr.value_type not in (ValueTypeEnum.INT, ValueTypeEnum.FLOAT) else field
            sorts.append({sort_by: {"order": sort_type}})

        self.query.update(dict(sort=sorts))

    def _paginate_build(self):
        self.query.update({"from": (self.page - 1) * self.count,
                           "size": self.count})

    def _fl_build(self):
        return ['hits.hits._source.{0}'.format(i) for i in self.fl]

    def search(self):
        try:
            numfound, cis, facet = self._query_build_raw()
        except Exception as e:
            current_app.logger.error(str(e))
            raise SearchError("unknown search error")

        total = len(cis)

        counter = dict()
        for ci in cis:
            ci_type = ci.get("ci_type")
            if ci_type not in counter.keys():
                counter[ci_type] = 0
            counter[ci_type] += 1

        facet_ = dict()
        for k in facet:
            facet_[k] = [[i['key'], i['doc_count'], k] for i in facet[k]["buckets"]]

        return cis, counter, total, self.page, numfound, facet_
