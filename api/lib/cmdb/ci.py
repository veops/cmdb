# -*- coding:utf-8 -*- 


import datetime
import json

from flask import abort
from flask import current_app
from werkzeug.exceptions import BadRequest

from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.cache import RelationTypeCache
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.history import CIRelationHistoryManager
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_IDS
from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_VALUE_TABLE
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.lib.utils import handle_arg_list
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CITypeAttribute
from api.tasks.cmdb import ci_cache
from api.tasks.cmdb import ci_delete
from api.tasks.cmdb import ci_relation_cache
from api.tasks.cmdb import ci_relation_delete


class CIManager(object):
    """ manage CI interface
    """

    def __init__(self):
        pass

    @staticmethod
    def get_type_name(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not existed".format(ci_id))
        return CITypeCache.get(ci.type_id).name

    @staticmethod
    def confirm_ci_existed(ci_id):
        CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not existed".format(ci_id))

    @classmethod
    def get_ci_by_id(cls, ci_id, ret_key=RetKey.NAME, fields=None, need_children=True):
        """
        
        :param ci_id: 
        :param ret_key: name, id, or alias
        :param fields:  attribute list
        :param need_children: 
        :return: 
        """

        ci = CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not existed".format(ci_id))

        res = dict()

        if need_children:
            children = CIRelationManager.get_children(ci_id, ret_key=ret_key)  # one floor
            res.update(children)

        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.name

        res.update(cls.get_cis_by_ids([str(ci_id)], fields=fields, ret_key=ret_key))

        res['_type'] = ci_type.id
        res['_id'] = ci_id

        return res

    @staticmethod
    def get_ci_by_id_from_db(ci_id, ret_key=RetKey.NAME, fields=None, need_children=True, use_master=False):
        """
        
        :param ci_id: 
        :param ret_key: name, id or alias
        :param fields: list
        :param need_children: 
        :param use_master: whether to use master db
        :return: 
        """

        ci = CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not existed".format(ci_id))

        res = dict()

        if need_children:
            children = CIRelationManager.get_children(ci_id, ret_key=ret_key)  # one floor
            res.update(children)

        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.name

        fields = CITypeAttributeManager.get_attr_names_by_type_id(ci.type_id) if not fields else fields
        unique_key = AttributeCache.get(ci_type.unique_id)
        _res = AttributeValueManager().get_attr_values(fields,
                                                       ci_id,
                                                       ret_key=ret_key,
                                                       unique_key=unique_key,
                                                       use_master=use_master)
        res.update(_res)

        res['type_id'] = ci_type.id
        res['ci_id'] = ci_id

        return res

    def get_ci_by_ids(self, ci_id_list, ret_key=RetKey.NAME, fields=None):
        return [self.get_ci_by_id(ci_id, ret_key=ret_key, fields=fields) for ci_id in ci_id_list]

    @classmethod
    def get_cis_by_type(cls, type_id, ret_key=RetKey.NAME, fields="", page=1, per_page=None):
        cis = db.session.query(CI.id).filter(CI.type_id == type_id).filter(CI.deleted.is_(False))
        numfound = cis.count()

        cis = cis.offset((page - 1) * per_page).limit(per_page)
        ci_ids = [str(ci.id) for ci in cis]
        res = cls.get_cis_by_ids(ci_ids, ret_key, fields)

        return numfound, page, res

    @staticmethod
    def ci_is_exist(unique_key, unique_value):
        """
        
        :param unique_key: is a attribute
        :param unique_value: 
        :return: 
        """
        value_table = TableMap(attr_name=unique_key.name).table
        unique = value_table.get_by(attr_id=unique_key.id,
                                    value=unique_value,
                                    to_dict=False,
                                    first=True)
        if unique:
            return CI.get_by_id(unique.ci_id)

    @staticmethod
    def _delete_ci_by_id(ci_id):
        ci = CI.get_by_id(ci_id)
        ci.delete()  # TODO: soft delete

    @classmethod
    def add(cls, ci_type_name, exist_policy=ExistPolicy.REPLACE, _no_attribute_policy=ExistPolicy.IGNORE, **ci_dict):
        """
        
        :param ci_type_name: 
        :param exist_policy: replace or reject or need
        :param _no_attribute_policy: ignore or reject
        :param ci_dict: 
        :return: 
        """

        ci_type = CITypeManager.check_is_existed(ci_type_name)

        unique_key = AttributeCache.get(ci_type.unique_id) or abort(400, 'illegality unique attribute')

        unique_value = ci_dict.get(unique_key.name)
        unique_value = unique_value or ci_dict.get(unique_key.alias)
        unique_value = unique_value or ci_dict.get(unique_key.id)
        unique_value = unique_value or abort(400, '{0} missing'.format(unique_key.name))

        existed = cls.ci_is_exist(unique_key, unique_value)
        if existed is not None:
            if exist_policy == ExistPolicy.REJECT:
                return abort(400, 'CI is already existed')
            if existed.type_id != ci_type.id:
                existed.update(type_id=ci_type.id)
            ci = existed
        else:
            if exist_policy == ExistPolicy.NEED:
                return abort(404, 'CI <{0}> does not exist'.format(unique_value))
            ci = CI.create(type_id=ci_type.id)

        value_manager = AttributeValueManager()
        for p, v in ci_dict.items():
            try:
                value_manager.create_or_update_attr_value(p, v, ci.id, _no_attribute_policy)
            except BadRequest as e:
                if existed is None:
                    cls.delete(ci.id)
                raise e

        ci_cache.apply_async([ci.id], queue=CMDB_QUEUE)

        return ci.id

    def update(self, ci_id, **ci_dict):
        self.confirm_ci_existed(ci_id)
        value_manager = AttributeValueManager()
        for p, v in ci_dict.items():
            try:
                value_manager.create_or_update_attr_value(p, v, ci_id)
            except BadRequest as e:
                raise e

        ci_cache.apply_async([ci_id], queue=CMDB_QUEUE)

    @staticmethod
    def update_unique_value(ci_id, unique_name, unique_value):
        CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not found".format(ci_id))

        AttributeValueManager().create_or_update_attr_value(unique_name, unique_value, ci_id)

        ci_cache.apply_async([ci_id], queue=CMDB_QUEUE)

    @staticmethod
    def delete(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, "CI <{0}> is not found".format(ci_id))

        attrs = CITypeAttribute.get_by(type_id=ci.type_id, to_dict=False)
        attr_names = set([AttributeCache.get(attr.attr_id).name for attr in attrs])
        for attr_name in attr_names:
            value_table = TableMap(attr_name=attr_name).table
            for item in value_table.get_by(ci_id=ci_id, to_dict=False):
                item.delete()

        for item in CIRelation.get_by(first_ci_id=ci_id, to_dict=False):
            ci_relation_delete.apply_async(args=(item.first_ci_id, item.second_ci_id), queue=CMDB_QUEUE)
            item.delete()

        for item in CIRelation.get_by(second_ci_id=ci_id, to_dict=False):
            ci_relation_delete.apply_async(args=(item.first_ci_id, item.second_ci_id), queue=CMDB_QUEUE)
            item.delete()

        ci.delete()  # TODO: soft delete

        AttributeHistoryManger.add(ci_id, [(None, OperateType.DELETE, None, None)])

        ci_delete.apply_async([ci.id], queue=CMDB_QUEUE)

        return ci_id

    @staticmethod
    def add_heartbeat(ci_type, unique_value):
        ci_type = CITypeManager().check_is_existed(ci_type)

        unique_key = AttributeCache.get(ci_type.unique_id)
        value_table = TableMap(attr_name=unique_key.name).table

        v = value_table.get_by(attr_id=unique_key.id,
                               value=unique_value,
                               to_dict=False,
                               first=True) \
            or abort(404, "not found")

        ci = CI.get_by_id(v.ci_id) or abort(404, "CI <{0}> is not found".format(v.ci_id))

        ci.update(heartbeat=datetime.datetime.now())

    @classmethod
    @kwargs_required("type_id", "page")
    def get_heartbeat(cls, **kwargs):
        query = db.session.query(CI.id, CI.heartbeat).filter(CI.deleted.is_(False))

        expire = datetime.datetime.now() - datetime.timedelta(minutes=72)
        type_ids = handle_arg_list(kwargs["type_id"])

        query = query.filter(CI.type_id.in_(type_ids))

        page = kwargs.get("page")
        agent_status = kwargs.get("agent_status")
        if agent_status == -1:
            query = query.filter(CI.heartbeat.is_(None))
        elif agent_status == 0:
            query = query.filter(CI.heartbeat <= expire)
        elif agent_status == 1:
            query = query.filter(CI.heartbeat > expire)

        numfound = query.count()
        per_page_count = current_app.config.get("DEFAULT_PAGE_COUNT")
        cis = query.offset((page - 1) * per_page_count).limit(per_page_count).all()
        ci_ids = [ci.id for ci in cis]
        heartbeat_dict = {}
        for ci in cis:
            if agent_status is not None:
                heartbeat_dict[ci.id] = agent_status
            else:
                if ci.heartbeat is None:
                    heartbeat_dict[ci.id] = -1
                elif ci.heartbeat <= expire:
                    heartbeat_dict[ci.id] = 0
                else:
                    heartbeat_dict[ci.id] = 1
        current_app.logger.debug(heartbeat_dict)
        ci_ids = list(map(str, ci_ids))
        res = cls.get_cis_by_ids(ci_ids, fields=["hostname", "private_ip"])
        result = [(i.get("hostname"), i.get("private_ip")[0], i.get("ci_type"),
                   heartbeat_dict.get(i.get("_id"))) for i in res
                  if i.get("private_ip")]
        return numfound, result

    @staticmethod
    def _get_cis_from_cache(ci_ids, ret_key=RetKey.NAME, fields=None):
        res = rd.get(ci_ids, REDIS_PREFIX_CI)
        if res is not None and None not in res and ret_key == RetKey.NAME:
            res = list(map(json.loads, res))
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
                return _res

    @staticmethod
    def _get_cis_from_db(ci_ids, ret_key=RetKey.NAME, fields=None, value_tables=None):
        if not fields:
            filter_fields_sql = ""
        else:
            _fields = list()
            for field in fields:
                attr = AttributeCache.get(field)
                if attr is not None:
                    _fields.append(str(attr.id))
            filter_fields_sql = "WHERE A.attr_id in ({0})".format(",".join(_fields))

        ci_ids = ",".join(ci_ids)
        if value_tables is None:
            value_tables = ValueTypeMap.table_name.values()

        value_sql = " UNION ".join([QUERY_CIS_BY_VALUE_TABLE.format(value_table, ci_ids)
                                    for value_table in value_tables])
        query_sql = QUERY_CIS_BY_IDS.format(filter_fields_sql, value_sql)
        # current_app.logger.debug(query_sql)
        cis = db.session.execute(query_sql).fetchall()
        ci_set = set()
        res = list()
        ci_dict = dict()
        for ci_id, type_id, attr_id, attr_name, attr_alias, value, value_type, is_list in cis:
            if ci_id not in ci_set:
                ci_dict = dict()
                ci_type = CITypeCache.get(type_id)
                ci_dict["ci_id"] = ci_id
                ci_dict["ci_type"] = type_id
                ci_dict["ci_type"] = ci_type.name
                ci_dict["ci_type_alias"] = ci_type.alias
                ci_set.add(ci_id)
                res.append(ci_dict)

            if ret_key == RetKey.NAME:
                attr_key = attr_name
            elif ret_key == RetKey.ALIAS:
                attr_key = attr_alias
            elif ret_key == RetKey.ID:
                attr_key = attr_id
            else:
                return abort(400, "invalid ret key")

            value = ValueTypeMap.serialize2[value_type](value)
            if is_list:
                ci_dict.setdefault(attr_key, []).append(value)
            else:
                ci_dict[attr_key] = value

        return res

    @classmethod
    def get_cis_by_ids(cls, ci_ids, ret_key=RetKey.NAME, fields=None, value_tables=None):
        """

        :param ci_ids: list of CI instance ID, eg. ['1', '2']
        :param ret_key: name, id or alias
        :param fields: 
        :param value_tables: 
        :return: 
        """

        if not ci_ids:
            return []

        fields = [] if fields is None or not isinstance(fields, list) else fields

        ci_id_tuple = tuple(map(int, ci_ids))
        res = cls._get_cis_from_cache(ci_id_tuple, ret_key, fields)
        if res is not None:
            return res

        current_app.logger.warning("cache not hit...............")
        return cls._get_cis_from_db(ci_ids, ret_key, fields, value_tables)


class CIRelationManager(object):
    """
    Manage relation between CIs
    """

    def __init__(self):
        pass

    @staticmethod
    def _get_default_relation_type():
        return RelationTypeCache.get("contain").id  # FIXME

    @classmethod
    def get_children(cls, ci_id, ret_key=RetKey.NAME):
        second_cis = CIRelation.get_by(first_ci_id=ci_id, to_dict=False)
        second_ci_ids = (second_ci.second_ci_id for second_ci in second_cis)
        ci_type2ci_ids = dict()
        for ci_id in second_ci_ids:
            type_id = CI.get_by_id(ci_id).type_id
            ci_type2ci_ids.setdefault(type_id, []).append(ci_id)

        res = {}
        for type_id in ci_type2ci_ids:
            ci_type = CITypeCache.get(type_id)
            children = CIManager.get_cis_by_ids(list(map(str, ci_type2ci_ids[type_id])), ret_key=ret_key)
            res[ci_type.name] = children
        return res

    def get_second_cis(self, first_ci_id, relation_type_id=None, page=1, per_page=None, **kwargs):
        second_cis = db.session.query(CI.id).filter(CI.deleted.is_(False)).join(
            CIRelation, CIRelation.second_ci_id == CI.id).filter(
            CIRelation.first_ci_id == first_ci_id)

        if relation_type_id is not None:
            second_cis = second_cis.filter(CIRelation.relation_type_id == relation_type_id)

        if kwargs:  # TODO: special for devices
            second_cis = self._query_wrap_for_device(second_cis, **kwargs)

        numfound = second_cis.count()
        if per_page != "all":
            second_cis = second_cis.offset((page - 1) * per_page).limit(per_page).all()
        ci_ids = [str(son.id) for son in second_cis]
        result = CIManager.get_cis_by_ids(ci_ids)

        return numfound, len(ci_ids), result

    @staticmethod
    def _sort_handler(sort_by, query_sql):

        if sort_by.startswith("+"):
            sort_type = "asc"
            sort_by = sort_by[1:]
        elif sort_by.startswith("-"):
            sort_type = "desc"
            sort_by = sort_by[1:]
        else:
            sort_type = "asc"
        attr = AttributeCache.get(sort_by)
        if attr is None:
            return query_sql

        attr_id = attr.id
        value_table = TableMap(attr_name=sort_by).table

        ci_table = query_sql.subquery()
        query_sql = db.session.query(ci_table.c.id, value_table.value).join(
            value_table, value_table.ci_id == ci_table.c.id).filter(
            value_table.attr_id == attr_id).filter(ci_table.deleted.is_(False)).order_by(
            getattr(value_table.value, sort_type)())

        return query_sql

    def _query_wrap_for_device(self, query_sql, **kwargs):
        _type = kwargs.pop("_type", False) or kwargs.pop("type", False) or kwargs.pop("ci_type", False)
        if _type:
            ci_type = CITypeCache.get(_type)
            if ci_type is None:
                return
            query_sql = query_sql.filter(CI.type_id == ci_type.id)

        for k, v in kwargs.items():
            attr = AttributeCache.get(k)
            if attr is None:
                continue

            value_table = TableMap(attr_name=k).table
            ci_table = query_sql.subquery()
            query_sql = db.session.query(ci_table.c.id).join(
                value_table, value_table.ci_id == ci_table.c.id).filter(
                value_table.attr_id == attr.id).filter(ci_table.deleted.is_(False)).filter(
                value_table.value.ilike(v.replace("*", "%")))

        # current_app.logger.debug(query_sql)
        sort_by = kwargs.pop("sort", "")
        if sort_by:
            query_sql = self._sort_handler(sort_by, query_sql)

        return query_sql

    @classmethod
    def get_first_cis(cls, second_ci, relation_type_id=None, page=1, per_page=None):
        first_cis = db.session.query(CIRelation.first_ci_id).filter(
            CIRelation.second_ci_id == second_ci).filter(CIRelation.deleted.is_(False))
        if relation_type_id is not None:
            first_cis = first_cis.filter(CIRelation.relation_type_id == relation_type_id)

        numfound = first_cis.count()
        if per_page != "all":
            first_cis = first_cis.offset((page - 1) * per_page).limit(per_page).all()

        first_ci_ids = [str(first_ci.first_ci_id) for first_ci in first_cis]
        result = CIManager.get_cis_by_ids(first_ci_ids)

        return numfound, len(first_ci_ids), result

    @classmethod
    def add(cls, first_ci_id, second_ci_id, more=None, relation_type_id=None):

        relation_type_id = relation_type_id or cls._get_default_relation_type()

        CIManager.confirm_ci_existed(first_ci_id)
        CIManager.confirm_ci_existed(second_ci_id)

        existed = CIRelation.get_by(first_ci_id=first_ci_id,
                                    second_ci_id=second_ci_id,
                                    to_dict=False,
                                    first=True)
        if existed is not None:
            if existed.relation_type_id != relation_type_id:
                existed.update(relation_type_id=relation_type_id)
                CIRelationHistoryManager().add(existed, OperateType.UPDATE)
        else:
            existed = CIRelation.create(first_ci_id=first_ci_id,
                                        second_ci_id=second_ci_id,
                                        relation_type_id=relation_type_id)
            CIRelationHistoryManager().add(existed, OperateType.ADD)

            ci_relation_cache.apply_async(args=(first_ci_id, second_ci_id), queue=CMDB_QUEUE)

        if more is not None:
            existed.upadte(more=more)

        return existed.id

    @staticmethod
    def delete(cr_id):
        cr = CIRelation.get_by_id(cr_id) or abort(404, "CIRelation <{0}> is not existed".format(cr_id))
        cr.soft_delete()

        his_manager = CIRelationHistoryManager()
        his_manager.add(cr, operate_type=OperateType.DELETE)

        ci_relation_delete.apply_async(args=(cr.first_ci_id, cr.second_ci_id), queue=CMDB_QUEUE)

        return cr_id

    @classmethod
    def delete_2(cls, first_ci_id, second_ci_id):
        cr = CIRelation.get_by(first_ci_id=first_ci_id,
                               second_ci_id=second_ci_id,
                               to_dict=False,
                               first=True)

        ci_relation_delete.apply_async(args=(first_ci_id, second_ci_id), queue=CMDB_QUEUE)

        return cls.delete(cr.cr_id)
