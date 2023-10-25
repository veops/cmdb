# -*- coding:utf-8 -*-


from __future__ import unicode_literals

import copy
import time

from flask import current_app
from flask_login import current_user
from jinja2 import Template

from api.extensions import db
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci.db.query_sql import FACET_QUERY
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CI_BY_ATTR_NAME
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CI_BY_ID
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CI_BY_NO_ATTR
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CI_BY_TYPE
from api.lib.cmdb.search.ci.db.query_sql import QUERY_UNION_CI_ATTRIBUTE_IS_NULL
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.lib.utils import handle_arg_list


class Search(object):
    def __init__(self, query=None,
                 fl=None,
                 facet_field=None,
                 page=1,
                 ret_key=RetKey.NAME,
                 count=1,
                 sort=None,
                 ci_ids=None,
                 excludes=None):
        self.orig_query = query
        self.fl = fl or []
        self.excludes = excludes or []
        self.facet_field = facet_field
        self.page = page
        self.ret_key = ret_key
        self.count = count
        self.sort = sort
        self.ci_ids = ci_ids or []
        self.query_sql = ""
        self.type_id_list = []
        self.only_type_query = False

        self.valid_type_names = []
        self.type2filter_perms = dict()

    @staticmethod
    def _operator_proc(key):
        operator = "&"
        if key.startswith("+"):
            key = key[1:].strip()
        elif key.startswith("-~"):
            operator = "|~"
            key = key[2:].strip()
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
            return '_type', ValueTypeEnum.TEXT, operator, None

        if key in ('id', 'ci_id', '_id'):
            return '_id', ValueTypeEnum.TEXT, operator, None

        attr = AttributeCache.get(key)
        if attr:
            return attr.name, attr.value_type, operator, attr
        else:
            raise SearchError(ErrFormat.attribute_not_found.format(key))

    def _type_query_handler(self, v, queries):
        new_v = v[1:-1].split(";") if v.startswith("(") and v.endswith(")") else [v]
        for _v in new_v:
            ci_type = CITypeCache.get(_v)

            if len(new_v) == 1 and not self.sort and ci_type and ci_type.default_order_attr:
                self.sort = ci_type.default_order_attr

            if ci_type is not None:
                if self.valid_type_names == "ALL" or ci_type.name in self.valid_type_names:
                    self.type_id_list.append(str(ci_type.id))
                    if ci_type.id in self.type2filter_perms:
                        ci_filter = self.type2filter_perms[ci_type.id].get('ci_filter')
                        if ci_filter:
                            sub = []
                            ci_filter = Template(ci_filter).render(user=current_user)
                            for i in ci_filter.split(','):
                                if i.startswith("~") and not sub:
                                    queries.append(i)
                                else:
                                    sub.append(i)
                            if sub:
                                queries.append(dict(operator="&", queries=sub))

                        if self.type2filter_perms[ci_type.id].get('attr_filter'):
                            if not self.fl:
                                self.fl = set(self.type2filter_perms[ci_type.id]['attr_filter'])
                            else:
                                self.fl = set(self.fl) & set(self.type2filter_perms[ci_type.id]['attr_filter'])
                else:
                    raise SearchError(ErrFormat.no_permission.format(ci_type.alias, PermEnum.READ))
            else:
                raise SearchError(ErrFormat.ci_type_not_found2.format(_v))

        if self.type_id_list:
            type_ids = ",".join(self.type_id_list)
            _query_sql = QUERY_CI_BY_TYPE.format(type_ids)
            if self.only_type_query:
                return _query_sql
            else:
                return ""
        return ""

    @staticmethod
    def _id_query_handler(v):
        return QUERY_CI_BY_ID.format(v)

    @staticmethod
    def _in_query_handler(attr, v, is_not):
        new_v = v[1:-1].split(";")

        if attr.value_type == ValueTypeEnum.DATE:
            new_v = ["{} 00:00:00".format(i) for i in new_v if len(i) == 10]

        table_name = TableMap(attr=attr).table_name
        in_query = " OR {0}.value ".format(table_name).join(['{0} "{1}"'.format(
            "NOT LIKE" if is_not else "LIKE",
            _v.replace("*", "%")) for _v in new_v])
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(table_name, attr.id, in_query)
        return _query_sql

    @staticmethod
    def _range_query_handler(attr, v, is_not):
        start, end = [x.strip() for x in v[1:-1].split("_TO_")]

        if attr.value_type == ValueTypeEnum.DATE:
            start = "{} 00:00:00".format(start) if len(start) == 10 else start
            end = "{} 00:00:00".format(end) if len(end) == 10 else end

        table_name = TableMap(attr=attr).table_name
        range_query = "{0} '{1}' AND '{2}'".format(
            "NOT BETWEEN" if is_not else "BETWEEN",
            start.replace("*", "%"), end.replace("*", "%"))
        _query_sql = QUERY_CI_BY_ATTR_NAME.format(table_name, attr.id, range_query)
        return _query_sql

    @staticmethod
    def _comparison_query_handler(attr, v):
        table_name = TableMap(attr=attr).table_name
        if v.startswith(">=") or v.startswith("<="):
            if attr.value_type == ValueTypeEnum.DATE and len(v[2:]) == 10:
                v = "{} 00:00:00".format(v)

            comparison_query = "{0} '{1}'".format(v[:2], v[2:].replace("*", "%"))
        else:
            if attr.value_type == ValueTypeEnum.DATE and len(v[1:]) == 10:
                v = "{} 00:00:00".format(v)

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
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id IN ({0}) ".format(
                    ",".join(self.type_id_list)))

            return ret_sql.format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id IN ({3}) "
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

    def __sort_by_type(self, sort_type, query_sql):
        ret_sql = "SELECT SQL_CALC_FOUND_ROWS DISTINCT B.ci_id FROM ({0}) AS B {1}"

        if self.type_id_list:
            self.query_sql = "SELECT B.ci_id FROM ({0}) AS B {1}".format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id IN ({0}) ".format(
                    ",".join(self.type_id_list)))

            return ret_sql.format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id WHERE c_cis.type_id IN ({3}) "
                "ORDER BY c_cis.type_id {1} LIMIT {0:d}, {2};".format(
                    (self.page - 1) * self.count, sort_type, self.count, ",".join(self.type_id_list)))

        else:
            self.query_sql = "SELECT B.ci_id FROM ({0}) AS B {1}".format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id ")

            return ret_sql.format(
                query_sql,
                "INNER JOIN c_cis on c_cis.id=B.ci_id "
                "ORDER BY c_cis.type_id {1} LIMIT {0:d}, {2};".format(
                    (self.page - 1) * self.count, sort_type, self.count))

    def __sort_by_field(self, field, sort_type, query_sql):
        attr = AttributeCache.get(field)
        attr_id = attr.id

        table_name = TableMap(attr=attr).table_name
        _v_query_sql = """SELECT {0}.ci_id, {1}.value
                          FROM ({2}) AS {0} INNER JOIN {1} ON {1}.ci_id = {0}.ci_id
                          WHERE {1}.attr_id = {3}""".format("ALIAS", table_name, query_sql, attr_id)
        new_table = _v_query_sql

        if self.only_type_query or not self.type_id_list:
            return ("SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id FROM ({0}) AS C ORDER BY C.value {2} "
                    "LIMIT {1:d}, {3};".format(new_table, (self.page - 1) * self.count, sort_type, self.count))

        elif self.type_id_list:
            self.query_sql = """SELECT C.ci_id
                                FROM ({0}) AS C
                                INNER JOIN c_cis on c_cis.id=C.ci_id
                                WHERE c_cis.type_id IN ({1})""".format(new_table, ",".join(self.type_id_list))

            return """SELECT SQL_CALC_FOUND_ROWS DISTINCT C.ci_id
                      FROM ({0}) AS C
                      INNER JOIN c_cis on c_cis.id=C.ci_id
                      WHERE c_cis.type_id IN ({4})
                      ORDER BY C.value {2}
                      LIMIT {1:d}, {3};""".format(new_table,
                                                  (self.page - 1) * self.count,
                                                  sort_type, self.count,
                                                  ",".join(self.type_id_list))

    def _sort_query_handler(self, field, query_sql):

        field, sort_type = self.__sort_by(field)

        if field in ("_id", "ci_id") or not field:
            return self.__sort_by_id(sort_type, query_sql)
        elif field in ("_type", "ci_type"):
            return self.__sort_by_type(sort_type, query_sql)
        else:
            return self.__sort_by_field(field, sort_type, query_sql)

    @staticmethod
    def _wrap_sql(operator, alias, _query_sql, query_sql):
        if operator == "&":
            query_sql = """SELECT * FROM ({0}) as {1}
                           INNER JOIN ({2}) as {3} USING(ci_id)""".format(query_sql, alias, _query_sql, alias + "A")

        elif operator == "|" or operator == "|~":
            query_sql = "SELECT * FROM ({0}) as {1} UNION ALL ({2})".format(query_sql, alias, _query_sql)

        elif operator == "~":
            query_sql = """SELECT * FROM ({0}) as {1} LEFT JOIN ({2}) as {3} USING(ci_id)
                           WHERE {3}.ci_id is NULL""".format(query_sql, alias, _query_sql, alias + "A")

        return query_sql

    def _execute_sql(self, query_sql):
        v_query_sql = self._sort_query_handler(self.sort, query_sql)

        start = time.time()
        execute = db.session.execute
        # current_app.logger.debug(v_query_sql)
        res = execute(v_query_sql).fetchall()
        end_time = time.time()
        current_app.logger.debug("query ci ids time is: {0}".format(end_time - start))

        numfound = execute("SELECT FOUND_ROWS();").fetchall()[0][0]
        current_app.logger.debug("statistics ci ids time is: {0}".format(time.time() - end_time))

        return numfound, res

    def __get_types_has_read(self):
        """
        :return: _type:(type1;type2)
        """
        acl = ACLManager('cmdb')
        res = acl.get_resources(ResourceTypeEnum.CI)

        self.valid_type_names = {i['name'] for i in res if PermEnum.READ in i['permissions']}

        res2 = acl.get_resources(ResourceTypeEnum.CI_FILTER)
        if res2:
            self.type2filter_perms = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res2])))

        return "_type:({})".format(";".join(self.valid_type_names))

    def __confirm_type_first(self, queries):

        has_type = False

        result = []
        sub = {}
        id_query = None
        for q in queries:
            if q.startswith("_type"):
                has_type = True
                result.insert(0, q)
                if len(queries) == 1 or queries[1].startswith("-") or queries[1].startswith("~"):
                    self.only_type_query = True
            elif q.startswith("_id") and len(q.split(':')) == 2:
                id_query = int(q.split(":")[1]) if q.split(":")[1].isdigit() else None
                result.append(q)
            elif q.startswith("(") or q[1:].startswith("(") or q[2:].startswith("("):
                if not q.startswith("("):
                    raise SearchError(ErrFormat.ci_search_Parentheses_invalid)

                operator, q = self._operator_proc(q)
                if q.endswith(")"):
                    result.append(dict(operator=operator, queries=[q[1:-1]]))

                sub = dict(operator=operator, queries=[q[1:]])
            elif q.endswith(")") and sub:
                sub['queries'].append(q[:-1])
                result.append(copy.deepcopy(sub))
                sub = {}
            elif sub:
                sub['queries'].append(q)
            else:
                result.append(q)

        _is_app_admin = is_app_admin('cmdb') or current_user.username == "worker"
        if result and not has_type and not _is_app_admin:
            type_q = self.__get_types_has_read()
            if id_query:
                ci = CIManager.get_by_id(id_query)
                if not ci:
                    raise SearchError(ErrFormat.ci_not_found.format(id_query))
                result.insert(0, "_type:{}".format(ci.type_id))
            else:
                result.insert(0, type_q)
        elif _is_app_admin:
            self.valid_type_names = "ALL"
        else:
            self.__get_types_has_read()

        current_app.logger.warning(result)

        return result

    def __query_by_attr(self, q, queries, alias):
        k = q.split(":")[0].strip()
        v = "\:".join(q.split(":")[1:]).strip()
        v = v.replace("'", "\\'")
        v = v.replace('"', '\\"')
        field, field_type, operator, attr = self._attr_name_proc(k)
        if field == "_type":
            _query_sql = self._type_query_handler(v, queries)

        elif field == "_id":
            _query_sql = self._id_query_handler(v)

        elif field:
            if attr is None:
                raise SearchError(ErrFormat.attribute_not_found.format(field))

            is_not = True if operator == "|~" else False

            if field_type == ValueTypeEnum.DATE and len(v) == 10:
                v = "{} 00:00:00".format(v)

            # in query
            if v.startswith("(") and v.endswith(")"):
                _query_sql = self._in_query_handler(attr, v, is_not)
            # range query
            elif v.startswith("[") and v.endswith("]") and "_TO_" in v:
                _query_sql = self._range_query_handler(attr, v, is_not)
            # comparison query
            elif v.startswith(">=") or v.startswith("<=") or v.startswith(">") or v.startswith("<"):
                _query_sql = self._comparison_query_handler(attr, v)
            else:
                table_name = TableMap(attr=attr).table_name
                if is_not and v == "*" and self.type_id_list:  # special handle
                    _query_sql = QUERY_UNION_CI_ATTRIBUTE_IS_NULL.format(
                        ",".join(self.type_id_list),
                        table_name,
                        attr.id,
                        alias,
                        alias + 'A'
                    )
                    alias += "AA"
                else:
                    _query_sql = QUERY_CI_BY_ATTR_NAME.format(
                        table_name,
                        attr.id,
                        '{0} "{1}"'.format("NOT LIKE" if is_not else "LIKE", v.replace("*", "%")))
        else:
            raise SearchError(ErrFormat.argument_invalid.format("q"))

        return alias, _query_sql, operator

    def __query_build_by_field(self, queries, is_first=True, only_type_query_special=True, alias='A', operator='&'):
        query_sql = ""

        for q in queries:
            _query_sql = ""
            if isinstance(q, dict):
                alias, _query_sql, operator = self.__query_build_by_field(q['queries'], True, True, alias)
                current_app.logger.info(_query_sql)
                current_app.logger.info((operator, is_first, alias))
                operator = q['operator']

            elif ":" in q and not q.startswith("*"):
                alias, _query_sql, operator = self.__query_by_attr(q, queries, alias)
            elif q == "*":
                continue
            elif q:
                q = q.replace("'", "\\'")
                q = q.replace('"', '\\"')
                q = q.replace("*", "%").replace('\\n', '%')
                _query_sql = QUERY_CI_BY_NO_ATTR.format(q, alias)

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

        return alias, query_sql, operator

    def _filter_ids(self, query_sql):
        if self.ci_ids:
            return "SELECT * FROM ({0}) AS IN_QUERY WHERE IN_QUERY.ci_id IN ({1})".format(
                query_sql, ",".join(list(map(str, self.ci_ids))))

        return query_sql

    @staticmethod
    def _extra_handle_query_expr(args):  # \, or ,
        result = []
        if args:
            result.append(args[0])

        for arg in args[1:]:
            if result[-1].endswith('\\'):
                result[-1] = ",".join([result[-1].rstrip('\\'), arg])
            # elif ":" not in arg:
            #     result[-1] = ",".join([result[-1], arg])
            else:
                result.append(arg)

        return result

    def _query_build_raw(self):

        queries = handle_arg_list(self.orig_query)
        queries = self._extra_handle_query_expr(queries)
        queries = self.__confirm_type_first(queries)
        current_app.logger.debug(queries)

        _, query_sql, _ = self.__query_build_by_field(queries)

        s = time.time()
        if query_sql:
            query_sql = self._filter_ids(query_sql)
            self.query_sql = query_sql
            # current_app.logger.debug(query_sql)
            numfound, res = self._execute_sql(query_sql)
            current_app.logger.debug("query ci ids is: {0}".format(time.time() - s))
            return numfound, [_res[0] for _res in res]

        return 0, []

    def _facet_build(self):
        facet = {}
        for f in self.facet_field:
            k, field_type, _, attr = self._attr_name_proc(f)
            if k:
                table_name = TableMap(attr=attr).table_name
                query_sql = FACET_QUERY.format(table_name, self.query_sql, attr.id)
                result = db.session.execute(query_sql).fetchall()
                facet[k] = result

        facet_result = dict()
        for k, v in facet.items():
            if not k.startswith('_'):
                attr = AttributeCache.get(k)
                a = getattr(attr, self.ret_key)
                facet_result[a] = [(ValueTypeMap.serialize[attr.value_type](f[0]), f[1], a) for f in v]

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
            response = CIManager.get_cis_by_ids(ci_ids, ret_key=self.ret_key, fields=_fl, excludes=self.excludes)
        for res in response:
            ci_type = res.get("ci_type")
            if ci_type not in counter.keys():
                counter[ci_type] = 0
            counter[ci_type] += 1
        total = len(response)

        return response, counter, total, self.page, numfound, facet
