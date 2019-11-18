# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

import time

from flask import current_app

from api.extensions import db
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.const import TableMap
from api.lib.cmdb.search.db.query_sql import FACET_QUERY
from api.lib.cmdb.search.db.query_sql import QUERY_CI_BY_ATTR_NAME
from api.lib.cmdb.search.db.query_sql import QUERY_CI_BY_TYPE
from api.lib.utils import handle_arg_list
from api.models.cmdb import Attribute
from api.models.cmdb import CI


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
        self.count = count
        self.sort = sort
        self.query_sql = ""
        self.type_id_list = []
        self.only_type_query = False

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

    def _attr_name_proc(self, key):
        operator, key = self._operator_proc(key)

        if key in ('ci_type', 'type', '_type'):
            return '_type', Attribute.TEXT, operator, None

        if key in ('id', 'ci_id', '_id'):
            return '_id', Attribute.TEXT, operator, None

        attr = AttributeCache.get(key)
        if attr:
            return attr.name, attr.value_type, operator, attr
        else:
            raise SearchError("{0} is not existed".format(key))

    def _type_query_handler(self, v):
        new_v = v[1:-1].split(";") if v.startswith("(") and v.endswith(")") else [v]
        for _v in new_v:
            ci_type = CITypeCache.get(_v)
            if ci_type is not None:
                self.type_id_list.append(str(ci_type.id))

        if self.type_id_list:
            type_ids = ",".join(self.type_id_list)
            _query_sql = QUERY_CI_BY_TYPE.format(type_ids)
            if self.only_type_query:
                return _query_sql
            else:
                return ""
        return ""

    @staticmethod
    def _in_query_handler(attr, v):
        new_v = v[1:-1].split(";")
        table_name = TableMap(attr_name=attr.name).table_name
        in_query = " OR {0}.value ".format(table_name).join(['LIKE "{0}"'.format(_v.replace("*", "%")) for _v in new_v])
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(table_name, attr.id, in_query)
        return _query_sql

    @staticmethod
    def _range_query_handler(attr, v):
        start, end = [x.strip() for x in v[1:-1].split("_TO_")]
        table_name = TableMap(attr_name=attr.name).table_name
        range_query = "BETWEEN '{0}' AND '{1}'".format(start.replace("*", "%"), end.replace("*", "%"))
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(table_name, attr.id, range_query)
        return _query_sql

    @staticmethod
    def _comparison_query_handler(attr, v):
        table_name = TableMap(attr_name=attr.name).table_name
        if v.startswith(">=") or v.startswith("<="):
            comparison_query = "{0} '{1}'".format(v[:2], v[2:].replace("*", "%"))
        else:
            comparison_query = "{0} '{1}'".format(v[0], v[1:].replace("*", "%"))
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(table_name, attr.id, comparison_query)
        return _query_sql

    @staticmethod
    def __sort_by(field):
        field = field or ""
        sort_type = "ASC"
        if field.startswith("+"):
            field = field[1:]
        elif field.startswith("-"):
            field = field[1:]
            sort_type = "DESC"
        return field, sort_type

    def __sort_by_id(self, sort_type, query_sql):
        ret_sql = "SELECT SQL_CALC_FOUND_ROWS DISTINCT B.ci_id FROM ({0}) AS B {1}"

        if self.only_type_query:
            return ret_sql.format(query_sql, "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format(
                (self.page - 1) * self.count, sort_type, self.count))

        elif self.type_id_list:
            self.query_sql = "SELECT B.ci_id FROM ({0}) AS B {1}".format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id in ({0}) ".format(
                    ",".join(self.type_id_list)))

            return ret_sql.format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id in ({3}) "
                "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format(
                    (self.page - 1) * self.count, sort_type, self.count, ",".join(self.type_id_list)))

        else:
            self.query_sql = "SELECT B.ci_id FROM ({0}) AS B {1}".format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id ")

            return ret_sql.format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id "
                "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format((self.page - 1) * self.count, sort_type, self.count))

    def __sort_by_field(self, field, sort_type, query_sql):
        attr = AttributeCache.get(field)
        attr_id = attr.id

        table_name = TableMap(attr_name=attr.name).table_name
        _v_query_sql = """SELECT {0}.ci_id, {1}.value 
                          FROM ({2}) AS {0} INNER JOIN {1} ON {1}.ci_id = {0}.ci_id
                          WHERE {1}.attr_id = {3}""".format("ALIAS", table_name, query_sql, attr_id)
        new_table = _v_query_sql

        if self.only_type_query or not self.type_id_list:
            return "SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id, C.value " \
                   "FROM ({0}) AS C " \
                   "ORDER BY C.value {2} " \
                   "LIMIT {1:d}, {3};".format(new_table, (self.page - 1) * self.count, sort_type, self.count)

        elif self.type_id_list:
            self.query_sql = """SELECT C.ci_id
                                FROM ({0}) AS C
                                INNER JOIN c_cis on c_cis.id=C.ci_id
                                WHERE c_cis.type_id in ({1})""".format(new_table, ",".join(self.type_id_list))

            return """SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id, C.value
                      FROM ({0}) AS C
                      INNER JOIN c_cis on c_cis.id=C.ci_id
                      WHERE c_cis.type_id in ({4})
                      ORDER BY C.value {2}
                      LIMIT {1:d}, {3};""".format(new_table,
                                                  (self.page - 1) * self.count,
                                                  sort_type, self.count,
                                                  ",".join(self.type_id_list))

    def _sort_query_handler(self, field, query_sql):

        field, sort_type = self.__sort_by(field)

        if field in ("_id", "ci_id") or not field:
            return self.__sort_by_id(sort_type, query_sql)
        else:
            return self.__sort_by_field(field, sort_type, query_sql)

    @staticmethod
    def _wrap_sql(operator, alias, _query_sql, query_sql):
        if operator == "&":
            query_sql = """SELECT * FROM ({0}) as {1}
                           INNER JOIN ({2}) as {3} USING(ci_id)""".format(query_sql, alias, _query_sql, alias + "A")

        elif operator == "|":
            query_sql = "SELECT * FROM ({0}) as {1} UNION ALL ({2})".format(query_sql, alias, _query_sql)

        elif operator == "~":
            query_sql = """SELECT * FROM ({0}) as {1} LEFT JOIN ({2}) as {3} USING(ci_id) 
                           WHERE {3}.ci_id is NULL""".format(query_sql, alias, _query_sql, alias + "A")

        return query_sql

    def _execute_sql(self, query_sql):
        v_query_sql = self._sort_query_handler(self.sort, query_sql)

        start = time.time()
        execute = db.session.execute
        current_app.logger.debug(v_query_sql)
        res = execute(v_query_sql).fetchall()
        end_time = time.time()
        current_app.logger.debug("query ci ids time is: {0}".format(end_time - start))

        numfound = execute("SELECT FOUND_ROWS();").fetchall()[0][0]
        current_app.logger.debug("statistics ci ids time is: {0}".format(time.time() - end_time))

        return numfound, res

    def __confirm_type_first(self, queries):
        for q in queries:
            if q.startswith("_type"):
                queries.remove(q)
                queries.insert(0, q)
                if len(queries) == 1 or queries[1].startswith("-") or queries[1].startswith("~"):
                    self.only_type_query = True
        return queries

    def __query_build_by_field(self, queries):
        query_sql, alias, operator = "", "A", "&"
        is_first, only_type_query_special = True, True

        for q in queries:
            _query_sql = ""
            if ":" in q:
                k = q.split(":")[0].strip()
                v = ":".join(q.split(":")[1:]).strip()
                current_app.logger.debug(v)
                field, field_type, operator, attr = self._attr_name_proc(k)
                if field == "_type":
                    _query_sql = self._type_query_handler(v)
                    current_app.logger.debug(_query_sql)
                elif field == "_id":  # exclude all others
                    ci = CI.get_by_id(v)
                    if ci is not None:
                        return 1, [str(v)]
                elif field:
                    if attr is None:
                        raise SearchError("{0} is not found".format(field))

                    # in query
                    if v.startswith("(") and v.endswith(")"):
                        _query_sql = self._in_query_handler(attr, v)
                    # range query
                    elif v.startswith("[") and v.endswith("]") and "_TO_" in v:
                        _query_sql = self._range_query_handler(attr, v)
                    # comparison query
                    elif v.startswith(">=") or v.startswith("<=") or v.startswith(">") or v.startswith("<"):
                        _query_sql = self._comparison_query_handler(attr, v)
                    else:
                        table_name = TableMap(attr_name=attr.name).table_name
                        _query_sql = QUERY_CI_BY_ATTR_NAME.format(
                            table_name, attr.id, 'LIKE "{0}"'.format(v.replace("*", "%")))
                else:
                    raise SearchError("argument q format invalid: {0}".format(q))
            elif q:
                raise SearchError("argument q format invalid: {0}".format(q))

            if is_first and _query_sql and not self.only_type_query:
                query_sql = "SELECT * FROM ({0}) AS {1}".format(_query_sql, alias)
                is_first = False
                alias += "A"
            elif self.only_type_query and only_type_query_special:
                is_first = False
                only_type_query_special = False
                query_sql = _query_sql
            elif _query_sql:
                query_sql = self._wrap_sql(operator, alias, _query_sql, query_sql)
                alias += "AA"
        return None, query_sql

    def _query_build_raw(self):

        queries = handle_arg_list(self.orig_query)
        queries = self.__confirm_type_first(queries)
        current_app.logger.debug(queries)

        ret, query_sql = self.__query_build_by_field(queries)
        if ret is not None:
            return ret, query_sql

        s = time.time()
        if query_sql:
            self.query_sql = query_sql
            current_app.logger.debug(query_sql)
            numfound, res = self._execute_sql(query_sql)
            current_app.logger.debug("query ci ids is: {0}".format(time.time() - s))
            return numfound, [_res[0] for _res in res]

        return 0, []

    def _facet_build(self):
        facet = {}
        for f in self.facet_field:
            k, field_type, _, attr = self._attr_name_proc(f)
            if k:
                table_name = TableMap(attr_name=k).table_name
                query_sql = FACET_QUERY.format(table_name, self.query_sql, attr.id)
                current_app.logger.debug(query_sql)
                result = db.session.execute(query_sql).fetchall()
                facet[k] = result

        facet_result = dict()
        for k, v in facet.items():
            if not k.startswith('_'):
                a = getattr(AttributeCache.get(k), self.ret_key)
                facet_result[a] = [(f[0], f[1], a) for f in v]

        return facet_result

    def _fl_build(self):
        _fl = list()
        for f in self.fl:
            k, _, _, _ = self._attr_name_proc(f)
            if k:
                _fl.append(k)

        return _fl

    def search(self):
        numfound, ci_ids = self._query_build_raw()
        ci_ids = list(map(str, ci_ids))

        _fl = self._fl_build()

        if self.facet_field and numfound:
            facet = self._facet_build()
        else:
            facet = dict()

        response, counter = [], {}
        if ci_ids:
            response = CIManager.get_cis_by_ids(ci_ids, ret_key=self.ret_key, fields=_fl)
        for res in response:
            ci_type = res.get("ci_type")
            if ci_type not in counter.keys():
                counter[ci_type] = 0
            counter[ci_type] += 1
        total = len(response)

        return response, counter, total, self.page, numfound, facet
