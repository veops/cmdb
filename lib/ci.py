# -*- coding:utf-8 -*- 


import uuid
import time
import datetime
import json

from flask import current_app
from flask import abort
from sqlalchemy import or_

from extensions import db
from extensions import rd
from models.ci import CI
from models.ci_relation import CIRelation
from models.ci_type import CITypeAttribute
from models.ci_type import CITypeCache
from models.ci_type import CITypeSpecCache
from models.history import CIAttributeHistory
from models.attribute import CIAttributeCache
from lib.const import TableMap
from lib.const import type_map
from lib.value import AttributeValueManager
from lib.history import CIAttributeHistoryManger
from lib.history import CIRelationHistoryManager
from lib.query_sql import QUERY_HOSTS_NUM_BY_PRODUCT
from lib.query_sql import QUERY_HOSTS_NUM_BY_BU
from lib.query_sql import QUERY_HOSTS_NUM_BY_PROJECT
from lib.query_sql import QUERY_CIS_BY_IDS
from lib.query_sql import QUERY_CIS_BY_VALUE_TABLE
from tasks.cmdb import ci_cache
from tasks.cmdb import ci_delete


class CIManager(object):
    """ manage CI interface
    """

    def __init__(self):
        pass

    def get_ci_by_id(self, ci_id, ret_key="name",
                     fields=None, need_children=True, use_master=False):
        """@params: `ret_key` is one of 'name', 'id', 'alias'
                    `fields` is list of attribute name/alias/id
        """
        ci = CI.query.get(ci_id) or \
            abort(404, "CI {0} is not existed".format(ci_id))

        res = dict()

        if need_children:
            children = self.get_children(ci_id, ret_key=ret_key)  # one floor
            res.update(children)
        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.type_name
        uniq_key = CIAttributeCache.get(ci_type.uniq_id)
        if not fields:   # fields are all attributes
            attr_ids = db.session.query(CITypeAttribute.attr_id).filter_by(
                type_id=ci.type_id)
            fields = [CIAttributeCache.get(_.attr_id).attr_name
                      for _ in attr_ids]

        if uniq_key.attr_name not in fields:
            fields.append(uniq_key.attr_name)
        if fields:
            value_manager = AttributeValueManager()
            _res = value_manager._get_attr_values(
                fields, ci_id,
                ret_key=ret_key, uniq_key=uniq_key, use_master=use_master)
            res.update(_res)
            res['_type'] = ci_type.type_id
            res['_id'] = ci_id
        return res

    def get_ci_by_ids(self, ci_id_list, ret_key="name", fields=None):
        result = list()
        for ci_id in ci_id_list:
            res = self.get_ci_by_id(ci_id, ret_key=ret_key, fields=fields)
            result.append(res)
        return result

    def get_children(self, ci_id, ret_key='name', relation_type="contain"):
        second_cis = db.session.query(CIRelation.second_ci_id).filter(
            CIRelation.first_ci_id == ci_id).filter(or_(
                CIRelation.relation_type == relation_type,
                CIRelation.relation_type == "deploy"))
        second_ci_ids = (second_ci.second_ci_id for second_ci in second_cis)
        ci_types = {}
        for ci_id in second_ci_ids:
            type_id = db.session.query(CI.type_id).filter(
                CI.ci_id == ci_id).first().type_id
            if type_id not in ci_types:
                ci_types[type_id] = [ci_id]
            else:
                ci_types[type_id].append(ci_id)
        res = {}
        for type_id in ci_types:
            ci_type = CITypeCache.get(type_id)
            children = get_cis_by_ids(map(str, ci_types.get(type_id)),
                                      ret_key=ret_key)
            res[ci_type.type_name] = children
        return res

    def get_cis_by_type(self, type_id, ret_key="name", fields="",
                        page=1, per_page=None):
        if per_page is None:
            per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
        cis = db.session.query(CI.ci_id).filter(CI.type_id == type_id)
        numfound = cis.count()
        cis = cis.offset((page - 1) * per_page).limit(per_page)
        res = list()
        ci_ids = [str(ci.ci_id) for ci in cis]
        if ci_ids:
            res = get_cis_by_ids(ci_ids, ret_key, fields)
        return numfound, page, res

    def ci_is_exist(self, ci_type, unique_key, unique):
        table = TableMap(attr_name=unique_key.attr_name).table
        unique = db.session.query(table).filter(
            table.attr_id == unique_key.attr_id).filter(
                table.value == unique).first()
        if unique:
            return db.session.query(CI).filter(
                CI.ci_id == unique.ci_id).first()

    def _delete_ci_by_id(self, ci_id):
        db.session.query(CI.ci_id).filter(CI.ci_id == ci_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("delete ci is error, {0}".format(str(e)))

    def add(self, ci_type_name, exist_policy="replace",
            _no_attribute_policy="ignore", **ci_dict):
        ci_existed = False
        ci_type = CITypeCache.get(ci_type_name) or \
            abort(404, "CIType {0} is not existed".format(ci_type_name))

        unique_key = CIAttributeCache.get(ci_type.uniq_id) \
            or abort(500, 'illegality unique attribute')

        unique = ci_dict.get(unique_key.attr_name) \
            or abort(500, '{0} missing'.format(unique_key.attr_name))

        old_ci = self.ci_is_exist(ci_type, unique_key, unique)
        if old_ci is not None:
            ci_existed = True
            if exist_policy == 'reject':
                return abort(500, 'CI is existed')
            if old_ci.type_id != ci_type.type_id:  # update ci_type
                old_ci.type_id = ci_type.type_id
                db.session.add(old_ci)
                db.session.flush()
            ci = old_ci
        else:
            if exist_policy == 'need':
                return abort(404, 'CI {0} not exist'.format(unique))
            ci = CI()
            ci.type_id = ci_type.type_id
            _uuid = uuid.uuid4().hex
            ci.uuid = _uuid
            ci.created_time = datetime.datetime.now()
            db.session.add(ci)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error('add CI error: {0}'.format(str(e)))
                return abort(500, 'add CI error')
        value_manager = AttributeValueManager()
        histories = list()
        for p, v in ci_dict.items():
            ret, res = value_manager.add_attr_value(
                p, v, ci.ci_id, ci_type,
                _no_attribute_policy=_no_attribute_policy,
                ci_existed=ci_existed)
            if not ret:
                db.session.rollback()
                if not ci_existed:
                    self.delete(ci.ci_id)
                current_app.logger.info(res)
                return abort(500, res)
            if res is not None:
                histories.append(res)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            if not ci_existed:  # only add
                self.delete(ci.ci_id)
            return abort(500, "add CI error")
        his_manager = CIAttributeHistoryManger()
        his_manager.add(ci.ci_id, histories)
        ci_cache.apply_async([ci.ci_id], queue="cmdb_async")
        return ci.ci_id

    def delete(self, ci_id):
        ci = db.session.query(CI).filter(CI.ci_id == ci_id).first()
        if ci is not None:
            attrs = db.session.query(CITypeAttribute.attr_id).filter(
                CITypeAttribute.type_id == ci.type_id).all()
            attr_names = []
            for attr in attrs:
                attr_names.append(CIAttributeCache.get(attr.attr_id).attr_name)
            attr_names = set(attr_names)
            for attr_name in attr_names:
                Table = TableMap(attr_name=attr_name).table
                db.session.query(Table).filter(Table.ci_id == ci_id).delete()
            db.session.query(CIRelation).filter(
                CIRelation.first_ci_id == ci_id).delete()
            db.session.query(CIRelation).filter(
                CIRelation.second_ci_id == ci_id).delete()
            db.session.query(CIAttributeHistory).filter(
                CIAttributeHistory.ci_id == ci_id).delete()

            db.session.flush()
            db.session.delete(ci)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error("delete CI error, {0}".format(str(e)))
                return abort(500, "delete CI error, {0}".format(str(e)))
            # TODO: write history
            ci_delete.apply_async([ci.ci_id], queue="cmdb_async")
            return ci_id
        return abort(404, "CI {0} not found".format(ci_id))

    def add_heartbeat(self, ci_type, unique):
        ci_type = CITypeCache.get(ci_type)
        if not ci_type:
            return 'error'
        uniq_key = CIAttributeCache.get(ci_type.uniq_id)
        Table = TableMap(attr_name=uniq_key.attr_name).table
        ci_id = db.session.query(Table.ci_id).filter(
            Table.attr_id == uniq_key.attr_id).filter(
                Table.value == unique).first()
        if ci_id is None:
            return 'error'
        ci = db.session.query(CI).filter(CI.ci_id == ci_id.ci_id).first()
        if ci is None:
            return 'error'

        ci.heartbeat = datetime.datetime.now()

        db.session.add(ci)
        db.session.commit()
        return "ok"

    def get_heartbeat(self, page, type_id, agent_status=None):
        query = db.session.query(CI.ci_id, CI.heartbeat)
        expire = datetime.datetime.now() - datetime.timedelta(minutes=72)
        if type_id:
            query = query.filter(CI.type_id == type_id)
        else:
            query = query.filter(db.or_(CI.type_id == 7, CI.type_id == 8))
        if agent_status == -1:
            query = query.filter(CI.heartbeat == None)
        elif agent_status == 0:
            query = query.filter(CI.heartbeat <= expire)
        elif agent_status == 1:
            query = query.filter(CI.heartbeat > expire)
        numfound = query.count()
        per_page_count = current_app.config.get("DEFAULT_PAGE_COUNT")
        cis = query.offset((page - 1) * per_page_count).limit(
            per_page_count).all()
        ci_ids = [ci.ci_id for ci in cis]
        heartbeat_dict = {}
        for ci in cis:
            if agent_status is not None:
                heartbeat_dict[ci.ci_id] = agent_status
            else:
                if ci.heartbeat is None:
                    heartbeat_dict[ci.ci_id] = -1
                elif ci.heartbeat <= expire:
                    heartbeat_dict[ci.ci_id] = 0
                else:
                    heartbeat_dict[ci.ci_id] = 1
        current_app.logger.debug(heartbeat_dict)
        ci_ids = map(str, ci_ids)
        res = get_cis_by_ids(ci_ids, fields=["hostname", "private_ip"])
        result = [(i.get("hostname"), i.get("private_ip")[0], i.get("ci_type"),
                   heartbeat_dict.get(i.get("_id"))) for i in res
                  if i.get("private_ip")]
        return numfound, result


class CIRelationManager(object):
    """
    manage relation between CIs
    """

    def __init__(self):
        pass

    @property
    def relation_types(self):
        """ all CIType relation types
        """
        from lib.const import CI_RELATION_TYPES

        return CI_RELATION_TYPES

    def get_second_cis(self, first_ci, relation_type="contain",
                       page=1, per_page=None, **kwargs):
        if per_page is None:
            per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
        second_cis = db.session.query(
            CI.ci_id).join(
                CIRelation, CIRelation.second_ci_id == CI.ci_id).filter(
                    CIRelation.first_ci_id == first_ci).filter(
                        CIRelation.relation_type == relation_type)
        if kwargs:  # special for devices
            second_cis = self._query_wrap_for_device(second_cis, **kwargs)
        numfound = second_cis.count()
        second_cis = second_cis.offset(
            (page - 1) * per_page).limit(per_page).all()
        ci_ids = [str(son.ci_id) for son in second_cis]
        total = len(ci_ids)
        result = get_cis_by_ids(ci_ids)
        return numfound, total, result

    def get_grandsons(self, ci_id, page=1, per_page=None, **kwargs):
        if per_page is None:
            per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
        children = db.session.query(CIRelation.second_ci_id).filter(
            CIRelation.first_ci_id == ci_id).subquery()
        grandsons = db.session.query(CIRelation.second_ci_id).join(
            children,
            children.c.second_ci_id == CIRelation.first_ci_id).subquery()
        grandsons = db.session.query(CI.ci_id).join(
            grandsons, grandsons.c.second_ci_id == CI.ci_id)
        if kwargs:
            grandsons = self._query_wrap_for_device(grandsons, **kwargs)

        numfound = grandsons.count()
        grandsons = grandsons.offset(
            (page - 1) * per_page).limit(per_page).all()
        if not grandsons:
            return 0, 0, []
        ci_ids = [str(son.ci_id) for son in grandsons]
        total = len(ci_ids)
        result = get_cis_by_ids(ci_ids)

        return numfound, total, result

    def _sort_handler(self, sort_by, query_sql):

        if sort_by.startswith("+"):
            sort_type = "asc"
            sort_by = sort_by[1:]
        elif sort_by.startswith("-"):
            sort_type = "desc"
            sort_by = sort_by[1:]
        else:
            sort_type = "asc"
        attr = CIAttributeCache.get(sort_by)
        if attr is None:
            return query_sql

        attr_id = attr.attr_id
        Table = TableMap(attr_name=sort_by).table

        CI_table = query_sql.subquery()
        query_sql = db.session.query(CI_table.c.ci_id, Table.value).join(
            Table, Table.ci_id == CI_table.c.ci_id).filter(
                Table.attr_id == attr_id).order_by(
                    getattr(Table.value, sort_type)())

        return query_sql

    def _query_wrap_for_device(self, query_sql, **kwargs):
        _type = kwargs.pop("_type", False) or kwargs.pop("type", False) \
            or kwargs.pop("ci_type", False)
        if _type:
            ci_type = CITypeCache.get(_type)
            if ci_type is None:
                return
            query_sql = query_sql.filter(CI.type_id == ci_type.type_id)

        for k, v in kwargs.iteritems():
            attr = CIAttributeCache.get(k)
            if attr is None:
                continue
            Table = TableMap(attr_name=k).table
            CI_table = query_sql.subquery()
            query_sql = db.session.query(CI_table.c.ci_id).join(
                Table, Table.ci_id == CI_table.c.ci_id).filter(
                    Table.attr_id == attr.attr_id).filter(
                        Table.value.ilike(v.replace("*", "%")))

        current_app.logger.debug(query_sql)
        sort_by = kwargs.pop("sort", False)
        if sort_by:
            query_sql = self._sort_handler(sort_by, query_sql)
        return query_sql

    def get_great_grandsons(self, ci_id, page=1, per_page=None, **kwargs):
        if per_page is None:
            per_page = current_app.config.get("DEFAULT_PAGE_COUNT")

        children = db.session.query(CIRelation.second_ci_id).filter(
            CIRelation.first_ci_id == ci_id).subquery()
        grandsons = db.session.query(CIRelation.second_ci_id).join(
            children,
            children.c.second_ci_id == CIRelation.first_ci_id).subquery()
        great_grandsons = db.session.query(CIRelation.second_ci_id).join(
            grandsons,
            grandsons.c.second_ci_id == CIRelation.first_ci_id).subquery()
        great_grandsons = db.session.query(CI.ci_id).join(
            great_grandsons, great_grandsons.c.second_ci_id == CI.ci_id)
        if kwargs:
            great_grandsons = self._query_wrap_for_device(
                great_grandsons, **kwargs)
        if great_grandsons is None:
            return 0, 0, []
        numfound = great_grandsons.count()
        great_grandsons = great_grandsons.offset(
            (page - 1) * per_page).limit(per_page).all()
        ci_ids = [str(son.ci_id) for son in great_grandsons]
        total = len(ci_ids)
        result = get_cis_by_ids(ci_ids)

        return numfound, total, result

    def get_first_cis(self, second_ci, relation_type="contain",
                      page=1, per_page=None):
        """only for CI Type
        """
        if per_page is None:
            per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
        first_cis = db.session.query(CIRelation.first_ci_id).filter(
            CIRelation.second_ci_id == second_ci).filter(
                CIRelation.relation_type == relation_type)
        numfound = first_cis.count()
        first_cis = first_cis.offset(
            (page - 1) * per_page).limit(per_page).all()
        result = []
        first_ci_ids = [str(first_ci.first_ci_id) for first_ci in first_cis]
        total = len(first_ci_ids)
        if first_ci_ids:
            result = get_cis_by_ids(first_ci_ids)
        return numfound, total, result

    def get_grandfather(self, ci_id, relation_type="contain"):
        """only for CI Type
        """
        grandfather = db.session.query(CIRelation.first_ci_id).filter(
            CIRelation.second_ci_id.in_(db.session.query(
                CIRelation.first_ci_id).filter(
                    CIRelation.second_ci_id == ci_id).filter(
                        CIRelation.relation_type == relation_type))).filter(
                            CIRelation.relation_type == relation_type).first()
        if grandfather:
            return CIManager().get_ci_by_id(grandfather.first_ci_id,
                                            need_children=False)

    def add(self, first_ci, second_ci, more=None, relation_type="contain"):
        ci = db.session.query(CI.ci_id).filter(CI.ci_id == first_ci).first()
        if ci is None:
            return abort(404, "first_ci {0} is not existed".format(first_ci))
        c = db.session.query(CI.ci_id).filter(CI.ci_id == second_ci).first()
        if c is None:
            return abort(404, "second_ci {0} is not existed".format(
                second_ci))
        existed = db.session.query(CIRelation.cr_id).filter(
            CIRelation.first_ci_id == first_ci).filter(
                CIRelation.second_ci_id == second_ci).first()
        if existed is not None:
            return existed.cr_id
        cr = CIRelation()
        cr.first_ci_id = first_ci
        cr.second_ci_id = second_ci
        if more is not None:
            cr.more = more
        cr.relation_type = relation_type
        db.session.add(cr)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("add CIRelation is error, {0}".format(
                str(e)))
            return abort(500, "add CIRelation is error, {0}".format(str(e)))
            # write history
        his_manager = CIRelationHistoryManager()
        his_manager.add(cr.cr_id, cr.first_ci_id, cr.second_ci_id,
                        relation_type, operate_type="add")
        return cr.cr_id

    def delete(self, cr_id):
        cr = db.session.query(CIRelation).filter(
            CIRelation.cr_id == cr_id).first()
        cr_id = cr.cr_id
        first_ci = cr.first_ci_id
        second_ci = cr.second_ci_id
        if cr is not None:
            db.session.delete(cr)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(
                    "delete CIRelation is error, {0}".format(str(e)))
                return abort(
                    500, "delete CIRelation is error, {0}".format(str(e)))
            his_manager = CIRelationHistoryManager()
            his_manager.add(cr_id, first_ci, second_ci,
                            cr.relation_type, operate_type="delete")
            return True
        return abort(404, "CI relation is not existed")

    def delete_2(self, first_ci, second_ci):
        cr = db.session.query(CIRelation).filter(
            CIRelation.first_ci_id == first_ci).filter(
                CIRelation.second_ci_id == second_ci).first()
        return self.delete(cr.cr_id)


class HostNumStatis(object):
    def __init__(self):
        pass

    def get_hosts_by_project(self, project_id_list=None):
        res = {}
        if not project_id_list:
            project = CITypeCache.get("project")
            projects = db.session.query(CI.ci_id).filter(
                CI.type_id == project.type_id).all()
            project_id_list = (project.ci_id for project in projects)
        project_id_list = map(str, project_id_list)
        project_ids = ",".join(project_id_list)
        nums = db.session.execute(QUERY_HOSTS_NUM_BY_PROJECT.format(
            "".join(["(", project_ids, ")"]))).fetchall()
        if nums:
            for ci_id in project_id_list:
                res[int(ci_id)] = 0
            for ci_id, num in nums:
                res[ci_id] = num
        return res

    def get_hosts_by_product(self, product_id_list=None):
        res = {}
        if not product_id_list:
            product = CITypeCache.get("product")
            products = db.session.query(CI.ci_id).filter(
                CI.type_id == product.type_id).all()
            product_id_list = (product.ci_id for product in products)
        product_id_list = map(str, product_id_list)
        product_ids = ",".join(product_id_list)
        nums = db.session.execute(QUERY_HOSTS_NUM_BY_PRODUCT.format(
            "".join(["(", product_ids, ")"]))).fetchall()
        if nums:
            for ci_id in product_id_list:
                res[int(ci_id)] = 0
            for ci_id, num in nums:
                res[ci_id] = num
        return res

    def get_hosts_by_bu(self, bu_id_list=None):
        res = {}
        if not bu_id_list:
            bu = CITypeCache.get("bu")
            bus = db.session.query(CI.ci_id).filter(
                CI.type_id == bu.type_id).all()
            bu_id_list = (bu.ci_id for bu in bus)
        bu_id_list = map(str, bu_id_list)
        bu_ids = ",".join(bu_id_list)
        current_app.logger.debug(QUERY_HOSTS_NUM_BY_BU.format(
            "".join(["(", bu_ids, ")"])))
        if not bu_ids:
            return res
        nums = db.session.execute(
            QUERY_HOSTS_NUM_BY_BU.format(
                "".join(["(", bu_ids, ")"]))).fetchall()
        if nums:
            for ci_id in bu_id_list:
                res[int(ci_id)] = 0
            for ci_id, num in nums:
                res[ci_id] = num
        return res


def get_cis_by_ids(ci_ids, ret_key="name", fields="", value_tables=None):
    """ argument ci_ids are string list of CI instance ID, eg. ['1', '2']
    """
    if not ci_ids:
        return []
    start = time.time()
    ci_id_tuple = tuple(map(int, ci_ids))
    res = rd.get(ci_id_tuple)
    if res is not None and None not in res and ret_key == "name":
        res = map(json.loads, res)
        if not fields:
            return res
        else:
            _res = []
            for d in res:
                _d = dict()
                _d["_id"], _d["_type"] = d.get("_id"), d.get("_type")
                _d["ci_type"] = d.get("ci_type")
                for field in fields:
                    _d[field] = d.get(field)
                _res.append(_d)
            current_app.logger.debug("filter time: %s" % (time.time() - start))
            return _res
    current_app.logger.warning("cache not hit...............")
    if not fields:
        _fields = ""
    else:
        _fields = list()
        for field in fields:
            attr = CIAttributeCache.get(field)
            if attr is not None:
                _fields.append(str(attr.attr_id))
        _fields = "WHERE A.attr_id in ({0})".format(",".join(_fields))
    ci_ids = ",".join(ci_ids)
    if value_tables is None:
        value_tables = type_map["table_name"].values()
    current_app.logger.debug(value_tables)
    value_sql = " UNION ".join([QUERY_CIS_BY_VALUE_TABLE.format(value_table,
                                                                ci_ids)
                                for value_table in value_tables])
    query_sql = QUERY_CIS_BY_IDS.format(ci_ids, _fields, value_sql)
    current_app.logger.debug(query_sql)
    start = time.time()
    hosts = db.session.execute(query_sql).fetchall()
    current_app.logger.info("get cis time is: {0}".format(
        time.time() - start))

    ci_list = set()
    res = list()
    ci_dict = dict()
    start = time.time()
    for ci_id, type_id, attr_id, attr_name, \
            attr_alias, value, value_type, is_multivalue in hosts:
        if ci_id not in ci_list:
            ci_dict = dict()
            ci_type = CITypeSpecCache.get(type_id)
            ci_dict["_id"] = ci_id
            ci_dict["_type"] = type_id
            ci_dict["ci_type"] = ci_type.type_name
            ci_dict["ci_type_alias"] = ci_type.type_alias
            ci_list.add(ci_id)
            res.append(ci_dict)
        if ret_key == "name":
            if is_multivalue:
                if isinstance(ci_dict.get(attr_name), list):
                    ci_dict[attr_name].append(value)
                else:
                    ci_dict[attr_name] = [value]
            else:
                ci_dict[attr_name] = value
        elif ret_key == "alias":
            if is_multivalue:
                if isinstance(ci_dict.get(attr_alias), list):
                    ci_dict[attr_alias].append(value)
                else:
                    ci_dict[attr_alias] = [value]
            else:
                ci_dict[attr_alias] = value
        elif ret_key == "id":
            if is_multivalue:
                if isinstance(ci_dict.get(attr_id), list):
                    ci_dict[attr_id].append(value)
                else:
                    ci_dict[attr_id] = [value]
            else:
                ci_dict[attr_id] = value

    current_app.logger.debug("result parser time is: {0}".format(
        time.time() - start))
    return res