# -*- coding:utf-8 -*- 


import time

from flask import current_app

from lib.const import TableMap
from models.attribute import CIAttributeCache
from models.ci_type import CITypeCache
from extensions import db
from models import CI
from lib.ci import get_cis_by_ids
from lib.query_sql import FACET_QUERY
from lib.query_sql import QUERY_CI_BY_TYPE
from lib.query_sql import QUERY_CI_BY_ATTR_NAME


class SearchError(Exception):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return self.v


class Search(object):
    def __init__(self, query=None, fl=None, facet_field=None,
                 page=1, ret_key="name", count=1, sort=None):
        self.orig_query = query
        self.fl = fl
        self.facet_field = facet_field
        self.page = page
        self.ret_key = ret_key
        try:
            self.count = int(count)
        except ValueError:
            self.count = current_app.config.get("DEFAULT_PAGE_COUNT")
        self.sort = sort
        self.query_sql = ""
        self.type_id_list = []

    def tor_proc(self, key):
        tor = list()
        if key.startswith("+"):
            tor.append('&')
            key = key[1:].strip()
        elif key.startswith("-"):
            tor.append('|')
            key = key[1:].strip()
        elif key.startswith("~"):
            tor.append('~')
            key = key[1:].strip()
        if not tor:
            tor = ['&', '']
        if len(tor) < 2:
            tor.append('')
        return tor, key

    def attr_name_proc(self, key):
        tor, key = self.tor_proc(key)
        if key in ('ci_type', 'type', '_type'):
            return '_type', 'text', tor, None
        if key in ('id', 'ci_id', '_id'):
            return '_id', 'text', tor, None
        attr = CIAttributeCache.get(key)
        if attr is not None:
            # if not attr.is_index:
            #     raise SearchError("{0} is not indexed".format(attr.attr_name))
            field_name = attr.attr_name
            return field_name, attr.value_type, tor, attr
        else:
            raise SearchError("{0} is not existed".format(key))

    def type_query_handler(self, v, only_type_query):
        new_v = [v]
        if v.startswith("(") and v.endswith(")"):
            new_v = v[1:-1].split(";")
        for _v in new_v:
            ci_type = CITypeCache.get(_v)
            if ci_type is not None:
                self.type_id_list.append(str(ci_type.type_id))
        if self.type_id_list:
            type_ids = ",".join(self.type_id_list)
            _query_sql = QUERY_CI_BY_TYPE.format(type_ids)
            if only_type_query:
                return _query_sql
            else:
                return ""
        return ""

    def in_query_handler(self, attr, v):
        new_v = v[1:-1].split(";")
        table_name = TableMap(attr_name=attr.attr_name).table_name
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(
            table_name, attr.attr_id,
            " OR {0}.value ".format(table_name).join(['LIKE "{0}"'.format(
                _v.replace("*", "%")) for _v in new_v]))
        return _query_sql

    def range_query_handler(self, attr, v):
        start, end = [x.strip() for x in v[1:-1].split("_TO_")]
        table_name = TableMap(attr_name=attr.attr_name).table_name
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(
            table_name, attr.attr_id, "BETWEEN '{0}' AND '{1}'".format(
                start.replace("*", "%"), end.replace("*", "%")))
        return _query_sql

    def comparison_query_handler(self, attr, v):
        table_name = TableMap(attr_name=attr.attr_name).table_name
        if (v.startswith("<") and not v.startswith("<=")) or \
                (v.startswith(">") and not v.startswith(">=")):
            _query_sql = QUERY_CI_BY_ATTR_NAME.format(
                table_name, attr.attr_id, "{0} '{1}'".format(
                    v[0], v[1:].replace("*", "%")))
        elif v.startswith(">=") or v.startswith("<="):
            _query_sql = QUERY_CI_BY_ATTR_NAME.format(
                table_name, attr.attr_id, "{0} '{1}'".format(
                    v[:2], v[2:].replace("*", "%")))
        return _query_sql

    def sort_query_handler(self, field, query_sql, only_type_query):
        if field is None:
            field = ""
        if field.startswith("+"):
            field = field[1:]
            sort_type = "ASC"
        elif field.startswith("-"):
            field = field[1:]
            sort_type = "DESC"
        else:
            sort_type = "ASC"

        if field in ("_id", "ci_id") or not field:
            if only_type_query:
                return """SELECT SQL_CALC_FOUND_ROWS DISTINCT B.ci_id
                FROM ({0}) AS B {1}""".format(
                    query_sql,
                    "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format(
                        (self.page - 1) * self.count, sort_type, self.count))
            elif self.type_id_list:
                return """SELECT SQL_CALC_FOUND_ROWS DISTINCT B.ci_id
                FROM ({0}) AS B {1}""".format(
                    query_sql,
                    "INNER JOIN cis on cis.ci_id=B.ci_id "
                    "WHERE cis.type_id in ({3}) "
                    "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format(
                        (self.page - 1) * self.count, sort_type, self.count,
                        ",".join(self.type_id_list)))
            else:
                return """SELECT SQL_CALC_FOUND_ROWS DISTINCT B.ci_id
                FROM ({0}) AS B {1}""".format(
                    query_sql,
                    "INNER JOIN cis on cis.ci_id=B.ci_id "
                    "ORDER BY B.ci_id {1} LIMIT {0:d}, {2};".format(
                        (self.page - 1) * self.count, sort_type, self.count))
        else:
            attr = CIAttributeCache.get(field)
            attr_id = attr.attr_id

            table_name = TableMap(attr_name=attr.attr_name).table_name
            _v_query_sql = """SELECT {0}.ci_id, {1}.value FROM
                ({2}) AS {0} INNER JOIN {1} ON {1}.ci_id = {0}.ci_id
                WHERE {1}.attr_id = {3}""".format("ALIAS", table_name,
                                                  query_sql, attr_id)
            new_table = _v_query_sql
            if only_type_query:
                return "SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id " \
                       "FROM ({0}) AS C " \
                       "ORDER BY C.value {2} " \
                       "LIMIT {1:d}, {3};".format(new_table,
                                                  (self.page - 1) * self.count,
                                                  sort_type, self.count)
            elif self.type_id_list:
                return """SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id
                    FROM ({0}) AS C
                    INNER JOIN cis on cis.ci_id=C.ci_id
                    WHERE cis.type_id in ({4})
                    ORDER BY C.value {2}
                    LIMIT {1:d}, {3};""".format(new_table,
                                                (self.page - 1) * self.count,
                                                sort_type, self.count,
                                                ",".join(self.type_id_list))
            else:
                return """SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id
                    FROM ({0}) AS C
                    ORDER BY C.value {2}
                    LIMIT {1:d}, {3};""".format(new_table,
                                                (self.page - 1) * self.count,
                                                sort_type, self.count)

    def _wrap_sql(self, tor, alias, _query_sql, query_sql):
        if tor[0] == "&":
            query_sql = """SELECT * FROM ({0}) as {1}
                INNER JOIN ({2}) as {3} USING(ci_id)""".format(
                query_sql, alias, _query_sql, alias + "A")
        elif tor[0] == "|":
            query_sql = "SELECT * FROM ({0}) as {1} UNION ALL ({2})".format(
                query_sql, alias, _query_sql)
        elif tor[0] == "~":
            query_sql = "SELECT * FROM ({0}) as {1} LEFT JOIN ({2}) as {3} " \
                        "USING(ci_id) WHERE {3}.ci_id is NULL".format(
                        query_sql, alias, _query_sql, alias + "A")
        return query_sql

    def _execute_sql(self, query_sql, only_type_query):
        v_query_sql = self.sort_query_handler(self.sort, query_sql,
                                              only_type_query)
        start = time.time()
        execute = db.session.execute
        current_app.logger.debug(v_query_sql)
        res = execute(v_query_sql).fetchall()
        end_time = time.time()
        current_app.logger.debug("query ci ids time is: {0}".format(
            end_time - start))
        numfound = execute("SELECT FOUND_ROWS();").fetchall()[0][0]
        current_app.logger.debug("statistics ci ids time is: {0}".format(
            time.time() - end_time)
        )
        return numfound, res

    def query_build_raw(self):
        query_sql, alias, tor = "", "A", ["&"]
        is_first = True
        only_type_query = False
        queries = self.orig_query.split(",")
        queries = filter(lambda x: x != "", queries)
        for q in queries:
            if q.startswith("_type"):
                queries.remove(q)
                queries.insert(0, q)
                if len(queries) == 1 or queries[1].startswith("-") or \
                        queries[1].startswith("~"):
                    only_type_query = True
                break
        current_app.logger.debug(queries)
        special = True
        for q in queries:
            _query_sql = ""
            if ":" in q:
                k = q.split(":")[0].strip()
                v = ":".join(q.split(":")[1:]).strip()
                current_app.logger.info(v)
                field, field_type, tor, attr = self.attr_name_proc(k)
                if field == "_type":
                    _query_sql = self.type_query_handler(v, only_type_query)
                    current_app.logger.debug(_query_sql)
                elif field == "_id":  # exclude all others
                    _ci_ids = [str(v)]
                    ci = db.session.query(CI.ci_id).filter(
                        CI.ci_id == int(v)).first()
                    if ci is not None:
                        return 1, _ci_ids
                elif field:
                    if attr is None:
                        raise SearchError("{0} is not found".format(field))
                    # in query
                    if v.startswith("(") and v.endswith(")"):
                        _query_sql = self.in_query_handler(attr, v)
                    # range query
                    elif v.startswith("[") and v.endswith("]") and "_TO_" in v:
                        _query_sql = self.range_query_handler(attr, v)
                    # comparison query
                    elif v.startswith(">=") or v.startswith("<=") or \
                            v.startswith(">") or v.startswith("<"):
                        _query_sql = self.comparison_query_handler(attr, v)
                    else:
                        table_name = \
                            TableMap(attr_name=attr.attr_name).table_name
                        _query_sql = QUERY_CI_BY_ATTR_NAME.format(
                            table_name, attr.attr_id,
                            'LIKE "{0}"'.format(v.replace("*", "%")))
                else:
                    return 0, []
            elif q:
                return 0, []

            if is_first and _query_sql and not only_type_query:
                query_sql = "SELECT * FROM ({0}) AS {1}".format(_query_sql,
                                                                alias)
                is_first = False
                alias += "A"
            elif only_type_query and special:
                is_first = False
                special = False
                query_sql = _query_sql
            elif _query_sql:
                query_sql = self._wrap_sql(tor, alias, _query_sql, query_sql)
                alias += "AA"

        _start = time.time()
        if query_sql:
            self.query_sql = query_sql
            current_app.logger.debug(query_sql)
            numfound, res = self._execute_sql(query_sql, only_type_query)
            current_app.logger.info("query ci ids is: {0}".format(
                time.time() - _start))
            return numfound, [_res[0] for _res in res]
        return 0, []

    def facet_build(self):
        facet = {}
        for f in self.facet_field:
            k, field_type, _, attr = self.attr_name_proc(f)
            if k:
                table_name = TableMap(attr_name=k).table_name
                query_sql = FACET_QUERY.format(
                    table_name, self.query_sql, attr.attr_id)
                result = db.session.execute(query_sql).fetchall()
                facet[k] = result
        facet_result = dict()
        for k, v in facet.items():
            if not k.startswith('_'):
                a = getattr(CIAttributeCache.get(k), "attr_%s" % self.ret_key)
                facet_result[a] = list()
                for f in v:
                    if f[1] != 0:
                        facet_result[a].append((f[0], f[1], a))
        return facet_result

    def fl_build(self):
        _fl = list()
        for f in self.fl:
            k, _, _, _ = self.attr_name_proc(f)
            if k:
                _fl.append(k)
        return _fl

    def search(self):
        numfound, ci_ids = self.query_build_raw()
        ci_ids = map(str, ci_ids)
        _fl = self.fl_build()

        if self.facet_field and numfound:
            facet = self.facet_build()
        else:
            facet = dict()

        response, counter = [], {}
        if ci_ids:
            response = get_cis_by_ids(ci_ids, ret_key=self.ret_key, fields=_fl)
        for res in response:
            ci_type = res.get("ci_type")
            if ci_type not in counter.keys():
                counter[ci_type] = 0
            counter[ci_type] += 1
        total = len(response)
        return response, counter, total, self.page, numfound, facet