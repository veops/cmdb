# -*- coding:utf-8 -*-


import copy
import datetime
import json
import redis_lock
import threading
from flask import abort
from flask import current_app
from flask_login import current_user
from sqlalchemy.orm import aliased
from werkzeug.exceptions import BadRequest

from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.cache import CMDBCounterCache
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.ci_type import CITypeUniqueConstraintManager
from api.lib.cmdb.const import AttributeDefaultValueEnum
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import RelationSourceEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.history import CIRelationHistoryManager
from api.lib.cmdb.history import CITriggerHistoryManager
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.lib.notify import notify_send
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.lib.perm.acl.cache import UserCache
from api.lib.secrets.inner import InnerCrypt
from api.lib.secrets.vault import VaultClient
from api.lib.utils import handle_arg_list
from api.lib.webhook import webhook_request
from api.models.cmdb import AttributeHistory
from api.models.cmdb import AutoDiscoveryCI
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CITypeRelation
from api.models.cmdb import CITypeTrigger
from api.tasks.cmdb import ci_cache
from api.tasks.cmdb import ci_delete
from api.tasks.cmdb import ci_delete_trigger
from api.tasks.cmdb import ci_relation_add
from api.tasks.cmdb import ci_relation_cache
from api.tasks.cmdb import ci_relation_delete
from api.tasks.cmdb import delete_id_filter

PASSWORD_DEFAULT_SHOW = "******"


class CIManager(object):
    """ manage CI interface
    """

    def __init__(self):
        pass

    @staticmethod
    def get_by_id(ci_id):
        return CI.get_by_id(ci_id)

    @staticmethod
    def get_type_name(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        return CITypeCache.get(ci.type_id).name

    @staticmethod
    def get_type(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        return CITypeCache.get(ci.type_id)

    @staticmethod
    def confirm_ci_existed(ci_id):
        return CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

    @classmethod
    def get_ci_by_id(cls, ci_id, ret_key=RetKey.NAME, fields=None, need_children=True):
        """

        :param ci_id:
        :param ret_key: name, id, or alias
        :param fields:  attribute list
        :param need_children:
        :return:
        """

        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        res = dict()

        need_children and res.update(CIRelationManager.get_children(ci_id, ret_key=ret_key))  # one floor

        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.name

        ci_list = cls.get_cis_by_ids([str(ci_id)], fields=fields, ret_key=ret_key)
        ci_list and res.update(ci_list[0])

        res['_type'] = ci_type.id
        res['_id'] = ci_id

        return res

    @classmethod
    def valid_ci_only_read(cls, ci):
        if is_app_admin("cmdb"):
            return

        validate_permission(CIManager.get_type_name(ci.id), ResourceTypeEnum.CI, PermEnum.READ, "cmdb")

        acl = ACLManager('cmdb')
        res = acl.get_resources(ResourceTypeEnum.CI_FILTER)

        if res and ci.type_id in CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res]))):
            return abort(403, ErrFormat.no_permission2)

    @classmethod
    def _valid_ci_for_no_read(cls, ci, ci_type=None):
        type_id = ci.type_id if ci else ci_type.id

        acl = ACLManager('cmdb')
        res = acl.get_resources(ResourceTypeEnum.CI_FILTER)

        type2filters = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res])), type_id=type_id)
        if res and type_id in type2filters:
            if type2filters[type_id].get('ci_filter') and ci:
                from api.lib.cmdb.search import SearchError
                from api.lib.cmdb.search.ci import search

                query = "_id:{},{}".format(ci.id, type2filters[type_id].get('ci_filter'))
                s = search(query)
                try:
                    response, _, _, _, _, _ = s.search()
                except SearchError as e:
                    current_app.logger.warning(e)
                    return abort(400, str(e))

                if not response:
                    return abort(403, ErrFormat.ci_filter_perm_ci_no_permission)

            return type2filters[type_id].get('attr_filter') or []

    @classmethod
    def get_ci_by_id_from_db(cls, ci_id, ret_key=RetKey.NAME, fields=None, need_children=True, use_master=False,
                             valid=False, enum_use_label=False):
        """

        :param ci_id:
        :param ret_key: name, id or alias
        :param fields: list
        :param need_children:
        :param use_master: whether to use master db
        :param valid:
        :param enum_use_label:
        :return:
        """

        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        valid and cls.valid_ci_only_read(ci)

        res = dict()

        need_children and res.update(CIRelationManager.get_children(ci_id, ret_key=ret_key))  # one floor

        ci_type = CITypeCache.get(ci.type_id)
        if not ci_type:
            return res

        res["ci_type"] = ci_type.name

        enum_map = dict()
        if not enum_use_label:
            fields = CITypeAttributeManager.get_attr_names_by_type_id(ci.type_id) if not fields else fields
        else:
            fields, enum_map = CITypeAttributeManager.get_attr_names_label_enum(
                ci.type_id) if not fields else (fields, {})
        unique_key = AttributeCache.get(ci_type.unique_id)
        _res = AttributeValueManager().get_attr_values(fields,
                                                       ci_id,
                                                       ret_key=ret_key,
                                                       unique_key=unique_key,
                                                       use_master=use_master,
                                                       enum_map=enum_map)
        res.update(_res)

        res['_type'] = ci_type.id
        res['ci_type_alias'] = ci_type.alias
        res['_id'] = ci_id
        res['_updated_at'] = str(ci.updated_at or '')
        res['_updated_by'] = ci.updated_by

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

    @classmethod
    def get_ad_statistics(cls):
        return CMDBCounterCache.get_adc_counter() or {}

    @staticmethod
    def ci_is_exist(unique_key, unique_value, type_id):
        """

        :param unique_key: is an attribute
        :param unique_value:
        :param type_id:
        :return:
        """
        value_table = TableMap(attr=unique_key).table

        unique = db.session.query(value_table).join(CI, CI.id == value_table.ci_id).filter(
            value_table.attr_id == unique_key.id).filter(value_table.value == unique_value).filter(
            CI.type_id == type_id).filter(CI.deleted.is_(False)).filter(value_table.deleted.is_(False)).first()

        if unique:
            return CI.get_by_id(unique.ci_id)

    @staticmethod
    def _delete_ci_by_id(ci_id):
        ci = CI.get_by_id(ci_id)
        ci.delete()  # TODO: soft delete

    @staticmethod
    def _valid_unique_constraint(type_id, ci_dict, ci_id=None):
        unique_constraints = CITypeUniqueConstraintManager.get_by_type_id(type_id)
        if not unique_constraints:
            return

        attr_ids = []
        for i in unique_constraints:
            attr_ids.extend(i.attr_ids)

        attrs = [AttributeCache.get(i) for i in set(attr_ids)]
        id2name = {i.id: i.name for i in attrs if i}
        not_existed_fields = list(set(id2name.values()) - set(ci_dict.keys()))
        if not_existed_fields and ci_id is not None:
            ci_dict = copy.deepcopy(ci_dict)
            ci_dict.update(AttributeValueManager().get_attr_values(not_existed_fields, ci_id))

        for constraint in unique_constraints:
            ci_ids = None
            for attr_id in constraint.attr_ids:
                value_table = TableMap(attr_name=id2name[attr_id]).table

                values = value_table.get_by(attr_id=attr_id,
                                            value=ci_dict.get(id2name[attr_id]),
                                            only_query=True).join(
                    CI, CI.id == value_table.ci_id).filter(CI.type_id == type_id)
                _ci_ids = set([i.ci_id for i in values])
                if ci_ids is None:
                    ci_ids = _ci_ids
                else:
                    ci_ids &= _ci_ids

            if ci_ids - (ci_id and {ci_id} or set()):
                return abort(400, ErrFormat.unique_constraint.format(
                    " - ".join([id2name[i] for i in constraint.attr_ids])))

    @staticmethod
    def _auto_inc_id(attr):
        db.session.commit()

        value_table = TableMap(attr_name=attr.name).table
        with redis_lock.Lock(rd.r, "auto_inc_id_{}".format(attr.name), expire=10):
            max_v = value_table.get_by(attr_id=attr.id, only_query=True).order_by(
                getattr(value_table, 'value').desc()).first()
            if max_v is not None:
                return int(max_v.value) + 1

        return 1

    @staticmethod
    def _reference_to_ci_id(attr, payload):
        def __unique_value2id(_type, _v):
            value_table = TableMap(attr_name=_type.unique_id).table
            ci = value_table.get_by(attr_id=attr.id, value=_v)
            if ci is not None:
                return ci.ci_id

            return abort(400, ErrFormat.ci_reference_invalid.format(attr.alias, _v))

        def __valid_reference_id_existed(_id, _type_id):
            ci = CI.get_by_id(_id) or abort(404, ErrFormat.ci_reference_not_found.format(attr.alias, _id))

            if ci.type_id != _type_id:
                return abort(400, ErrFormat.ci_reference_invalid.format(attr.alias, _id))

        if attr.name in payload:
            k, reference_value = attr.name, payload[attr.name]
        elif attr.alias in payload:
            k, reference_value = attr.alias, payload[attr.alias]
        else:
            return
        if not reference_value:
            return

        reference_type = None
        if isinstance(reference_value, list):
            for idx, v in enumerate(reference_value):
                if isinstance(v, dict) and v.get('unique'):
                    if reference_type is None:
                        reference_type = CITypeCache.get(attr.reference_type_id)
                    if reference_type is not None:
                        reference_value[idx] = __unique_value2id(reference_type, v)
                else:
                    __valid_reference_id_existed(v, attr.reference_type_id)

        elif isinstance(reference_value, dict) and reference_value.get('unique'):
            if reference_type is None:
                reference_type = CITypeCache.get(attr.reference_type_id)
            if reference_type is not None:
                reference_value = __unique_value2id(reference_type, reference_value)
        elif str(reference_value).isdigit():
            reference_value = int(reference_value)
            __valid_reference_id_existed(reference_value, attr.reference_type_id)

        payload[k] = reference_value

    @classmethod
    def add(cls, ci_type_name,
            exist_policy=ExistPolicy.REPLACE,
            _no_attribute_policy=ExistPolicy.IGNORE,
            is_auto_discovery=False,
            _is_admin=False,
            ticket_id=None,
            _sync=False,
            **ci_dict):
        """
        Create a new Configuration Item (CI) or update existing based on unique constraints.

        Handles complete CI creation workflow including validation, uniqueness checks,
        password encryption, computed attributes, relationship creation, and caching.

        Args:
            ci_type_name (str): Name of the CI type to create
            exist_policy (ExistPolicy): How to handle existing CIs (REPLACE/REJECT/NEED)
            _no_attribute_policy (ExistPolicy): How to handle unknown attributes (IGNORE/REJECT)
            is_auto_discovery (bool): Whether CI is created by auto-discovery process
            _is_admin (bool): Whether to skip permission checks
            ticket_id (int, optional): Associated ticket ID for audit trail
            _sync (bool): Whether to execute cache/relation tasks synchronously
            **ci_dict: CI attribute values as key-value pairs

        Returns:
            int: ID of the created or updated CI

        Raises:
            400: If unique constraints violated, required attributes missing, or validation fails
            403: If user lacks permissions for restricted attributes
            404: If CI type not found or referenced CI not exists
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ci_type = CITypeManager.check_is_existed(ci_type_name)
        raw_dict = copy.deepcopy(ci_dict)

        unique_key = AttributeCache.get(ci_type.unique_id) or abort(
            400, ErrFormat.unique_value_not_found.format("unique_id={}".format(ci_type.unique_id)))

        unique_value = None
        # primary key is not auto inc id
        if not (unique_key.default and unique_key.default.get('default') == AttributeDefaultValueEnum.AUTO_INC_ID):
            unique_value = ci_dict.get(unique_key.name) or ci_dict.get(unique_key.alias) or ci_dict.get(unique_key.id)
            unique_value = unique_value or abort(400, ErrFormat.unique_key_required.format(unique_key.name))

        attrs = CITypeAttributeManager.get_all_attributes(ci_type.id)
        ci_type_attrs_name = {attr.name: attr for _, attr in attrs}
        ci_type_attrs_alias = {attr.alias: attr for _, attr in attrs}
        ci_attr2type_attr = {type_attr.attr_id: type_attr for type_attr, _ in attrs}
        ci_type_attrs_name_alias = {**ci_type_attrs_name, **ci_type_attrs_alias}

        ci = None
        record_id = None
        password_dict = {}
        with redis_lock.Lock(rd.r, ci_type.name, expire=10):
            db.session.commit()

            if (unique_key.default and unique_key.default.get('default') == AttributeDefaultValueEnum.AUTO_INC_ID and
                    not ci_dict.get(unique_key.name)):
                ci_dict[unique_key.name] = cls._auto_inc_id(unique_key)
                current_app.logger.info(ci_dict[unique_key.name])
                unique_value = ci_dict[unique_key.name]

            existed = cls.ci_is_exist(unique_key, unique_value, ci_type.id)
            if existed is not None:
                if exist_policy == ExistPolicy.REJECT:
                    return abort(400, ErrFormat.ci_is_already_existed)

                if existed.type_id != ci_type.id:
                    existed.update(type_id=ci_type.id)
                ci = existed
            else:
                if exist_policy == ExistPolicy.NEED:
                    return abort(404, ErrFormat.ci_not_found.format("{}={}".format(unique_key.name, unique_value)))

            limit_attrs = cls._valid_ci_for_no_read(ci, ci_type) if not _is_admin else {}

            if existed is None:  # set default
                for type_attr, attr in attrs:
                    if attr.default and attr.default.get('default') is not None:
                        if attr.default.get('default') and attr.default.get('default') in (
                                AttributeDefaultValueEnum.CREATED_AT, AttributeDefaultValueEnum.UPDATED_AT):
                            ci_dict[attr.name] = now
                        elif (attr.default.get('default') == AttributeDefaultValueEnum.AUTO_INC_ID and
                              not ci_dict.get(attr.name)):
                            ci_dict[attr.name] = cls._auto_inc_id(attr)
                        elif ((attr.name not in ci_dict and attr.alias not in ci_dict) or (
                                ci_dict.get(attr.name) is None and ci_dict.get(attr.alias) is None)):
                            ci_dict[attr.name] = attr.default.get('default')

                    if (type_attr.is_required and not attr.is_computed and
                            (attr.name not in ci_dict and attr.alias not in ci_dict)):
                        return abort(400, ErrFormat.attribute_value_required.format(attr.name))
            else:
                for type_attr, attr in attrs:
                    if attr.default and attr.default.get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                        ci_dict[attr.name] = now

            value_manager = AttributeValueManager()

            computed_attrs = []
            for _, attr in attrs:
                if attr.is_computed:
                    computed_attrs.append(attr.to_dict())
                    ci_dict[attr.name] = None
                elif attr.is_password:
                    if attr.name in ci_dict:
                        password_dict[attr.id] = (ci_dict.pop(attr.name), attr.is_dynamic)
                    elif attr.alias in ci_dict:
                        password_dict[attr.id] = (ci_dict.pop(attr.alias), attr.is_dynamic)

                    if attr.re_check and password_dict.get(attr.id):
                        value_manager.check_re(attr.re_check, attr.alias, password_dict[attr.id][0])
                elif attr.is_reference:
                    cls._reference_to_ci_id(attr, ci_dict)

            cls._valid_unique_constraint(ci_type.id, ci_dict, ci and ci.id)

            ref_ci_dict = dict()
            for k in copy.deepcopy(ci_dict):
                if k.startswith("$") and "." in k:
                    ref_ci_dict[k] = ci_dict[k]
                    continue

                if k not in ci_type_attrs_name and (
                        k not in ci_type_attrs_alias and _no_attribute_policy == ExistPolicy.REJECT):
                    return abort(400, ErrFormat.attribute_not_found.format(k))

                _attr_name = ((ci_type_attrs_name.get(k) and ci_type_attrs_name[k].name) or
                              (ci_type_attrs_alias.get(k) and ci_type_attrs_alias[k].name))
                if limit_attrs and _attr_name not in limit_attrs:
                    if k in raw_dict:
                        return abort(403, ErrFormat.ci_filter_perm_attr_no_permission.format(k))
                    else:
                        ci_dict.pop(k)

            ci_dict = {ci_type_attrs_name_alias[k].name: v for k, v in ci_dict.items() if k in ci_type_attrs_name_alias}

            key2attr = value_manager.valid_attr_value(ci_dict, ci_type.id, ci and ci.id,
                                                      ci_type_attrs_name, ci_type_attrs_alias, ci_attr2type_attr)

            if computed_attrs:
                value_manager.handle_ci_compute_attributes(ci_dict, computed_attrs, ci)

            operate_type = OperateType.UPDATE if ci is not None else OperateType.ADD
            try:
                ci = ci or CI.create(type_id=ci_type.id, is_auto_discovery=is_auto_discovery)
                record_id, has_dynamic = value_manager.create_or_update_attr_value(
                    ci, ci_dict, key2attr, ticket_id=ticket_id)
            except BadRequest as e:
                if existed is None:
                    cls.delete(ci.id)
                raise e

        if password_dict:
            for attr_id in password_dict:
                record_id = cls.save_password(ci.id, attr_id, password_dict[attr_id], record_id, ci_type.id)

        if record_id or has_dynamic:  # has changed
            if not _sync:
                ci_cache.apply_async(args=(ci.id, operate_type, record_id), queue=CMDB_QUEUE)
            else:
                ci_cache(ci.id, operate_type, record_id)

        if ref_ci_dict:  # add relations
            if not _sync:
                ci_relation_add.apply_async(args=(ref_ci_dict, ci.id, current_user.uid), queue=CMDB_QUEUE)
            else:
                ci_relation_add(ref_ci_dict, ci.id, current_user.uid)

        return ci.id

    def update(self, ci_id, _is_admin=False, ticket_id=None, _sync=False, **ci_dict):
        """
        Update an existing Configuration Item with new attribute values.

        Performs comprehensive CI update including validation, constraint checks,
        password handling, computed attributes processing, and change tracking.

        Args:
            ci_id (int): ID of the CI to update
            _is_admin (bool): Whether to skip permission checks
            ticket_id (int, optional): Associated ticket ID for audit trail
            _sync (bool): Whether to execute cache/relation tasks synchronously
            **ci_dict: CI attribute values to update as key-value pairs

        Raises:
            400: If unique constraints violated or validation fails
            403: If user lacks permissions for restricted attributes
            404: If CI not found
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ci = self.confirm_ci_existed(ci_id)
        ci_type = ci.ci_type

        attrs = CITypeAttributeManager.get_all_attributes(ci.type_id)
        ci_type_attrs_name = {attr.name: attr for _, attr in attrs}
        ci_type_attrs_alias2name = {attr.alias: attr.name for _, attr in attrs}
        ci_dict = {ci_type_attrs_alias2name[k] if k in ci_type_attrs_alias2name else k: v for k, v in ci_dict.items()}

        raw_dict = copy.deepcopy(ci_dict)

        ci_attr2type_attr = {type_attr.attr_id: type_attr for type_attr, _ in attrs}
        unique_name = None
        for _, attr in attrs:
            if attr.default and attr.default.get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                ci_dict[attr.name] = now

            if attr.id == ci_type.unique_id:
                unique_name = attr.name

        value_manager = AttributeValueManager()

        password_dict = dict()
        computed_attrs = list()
        for _, attr in attrs:
            if attr.is_computed:
                computed_attrs.append(attr.to_dict())
                ci_dict[attr.name] = None
            elif attr.is_password:
                if attr.name in ci_dict:
                    password_dict[attr.id] = (ci_dict.pop(attr.name), attr.is_dynamic)
                elif attr.alias in ci_dict:
                    password_dict[attr.id] = (ci_dict.pop(attr.alias), attr.is_dynamic)

                if attr.re_check and password_dict.get(attr.id):
                    value_manager.check_re(attr.re_check, attr.alias, password_dict[attr.id][0])
            elif attr.is_reference:
                self._reference_to_ci_id(attr, ci_dict)

        limit_attrs = self._valid_ci_for_no_read(ci) if not _is_admin else {}

        record_id = None
        with redis_lock.Lock(rd.r, ci_type.name, expire=10):
            db.session.commit()

            self._valid_unique_constraint(ci.type_id, ci_dict, ci_id)

            ci_dict = {k: v for k, v in ci_dict.items() if k in ci_type_attrs_name}
            key2attr = value_manager.valid_attr_value(ci_dict, ci.type_id, ci.id, ci_type_attrs_name,
                                                      ci_attr2type_attr=ci_attr2type_attr,
                                                      unique_name=unique_name)

            if computed_attrs:
                value_manager.handle_ci_compute_attributes(ci_dict, computed_attrs, ci)

            if limit_attrs:
                for k in copy.deepcopy(ci_dict):
                    if k not in limit_attrs:
                        if k in raw_dict:
                            return abort(403, ErrFormat.ci_filter_perm_attr_no_permission.format(k))
                        else:
                            ci_dict.pop(k)

            try:
                record_id, has_dynamic = value_manager.create_or_update_attr_value(
                    ci, ci_dict, key2attr, ticket_id=ticket_id)
            except BadRequest as e:
                raise e

        if password_dict:
            for attr_id in password_dict:
                record_id = self.save_password(ci.id, attr_id, password_dict[attr_id], record_id, ci.type_id)

        u = UserCache.get(current_user.uid)
        ci.update(updated_at=now, updated_by=u and u.nickname)

        if record_id or has_dynamic:  # has changed
            if not _sync:
                ci_cache.apply_async(args=(ci_id, OperateType.UPDATE, record_id), queue=CMDB_QUEUE)
            else:
                ci_cache(ci_id, OperateType.UPDATE, record_id)

        ref_ci_dict = {k: v for k, v in ci_dict.items() if k.startswith("$") and "." in k}
        if ref_ci_dict:
            if not _sync:
                ci_relation_add.apply_async(args=(ref_ci_dict, ci.id), queue=CMDB_QUEUE)
            else:
                ci_relation_add(ref_ci_dict, ci.id)

        u = UserCache.get(current_user.uid)
        ci.update(updated_at=now, updated_by=u and u.nickname)

    @staticmethod
    def update_unique_value(ci_id, unique_name, unique_value):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        key2attr = {unique_name: AttributeCache.get(unique_name)}
        record_id, _ = AttributeValueManager().create_or_update_attr_value(ci, {unique_name: unique_value}, key2attr)

        ci_cache.apply_async(args=(ci_id, OperateType.UPDATE, record_id), queue=CMDB_QUEUE)

    @classmethod
    def delete(cls, ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        cls._valid_ci_for_no_read(ci)

        ci_dict = cls.get_cis_by_ids([ci_id])
        ci_dict = ci_dict and ci_dict[0]

        if ci_dict:
            triggers = CITriggerManager.get(ci_dict['_type'])
            for trigger in triggers:
                option = trigger['option']
                if not option.get('enable') or option.get('action') != OperateType.DELETE:
                    continue

                if option.get('filter') and not CITriggerManager.ci_filter(ci_dict.get('_id'), option['filter']):
                    continue

                ci_delete_trigger.apply_async(args=(trigger, OperateType.DELETE, ci_dict), queue=CMDB_QUEUE)

        attrs = [i for _, i in CITypeAttributeManager.get_all_attributes(type_id=ci.type_id)]
        for attr in attrs:
            value_table = TableMap(attr=attr).table
            for item in value_table.get_by(ci_id=ci_id, to_dict=False):
                item.delete(commit=False)

        for item in CIRelation.get_by(first_ci_id=ci_id, to_dict=False):
            ci_relation_delete.apply_async(
                args=(item.first_ci_id, item.second_ci_id, item.ancestor_ids), queue=CMDB_QUEUE)
            item.delete(commit=False)

        for item in CIRelation.get_by(second_ci_id=ci_id, to_dict=False):
            ci_relation_delete.apply_async(
                args=(item.first_ci_id, item.second_ci_id, item.ancestor_ids), queue=CMDB_QUEUE)
            item.delete(commit=False)

        ad_ci = AutoDiscoveryCI.get_by(ci_id=ci_id, to_dict=False, first=True)
        ad_ci and ad_ci.update(is_accept=False, accept_by=None, accept_time=None, filter_none=False, commit=False)

        ci.delete(commit=False)  # TODO: soft delete

        db.session.commit()

        if ci_dict:
            AttributeHistoryManger.add(None, ci_id, [(None, OperateType.DELETE, ci_dict, None)], ci.type_id)

        ci_delete.apply_async(args=(ci_id, ci.type_id), queue=CMDB_QUEUE)
        delete_id_filter.apply_async(args=(ci_id,), queue=CMDB_QUEUE)

        return ci_id

    @staticmethod
    def add_heartbeat(ci_type, unique_value):
        ci_type = CITypeManager().check_is_existed(ci_type)

        unique_key = AttributeCache.get(ci_type.unique_id)
        value_table = TableMap(attr=unique_key).table

        v = (value_table.get_by(attr_id=unique_key.id, value=unique_value, to_dict=False, first=True) or
             abort(404, ErrFormat.not_found))

        ci = CI.get_by_id(v.ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(v.ci_id)))

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
    def _get_cis_from_cache(ci_ids, ret_key=RetKey.NAME, fields=None, unique_required=False, excludes=None):
        res = rd.get(ci_ids, REDIS_PREFIX_CI)
        if res is not None and None not in res and ret_key == RetKey.NAME:
            res = list(map(json.loads, res))
            if not fields and not excludes:
                return res
            elif fields:
                _res = []
                for d in res:
                    if isinstance(fields, dict) and d.get("_type") not in fields:
                        _res.append(d)
                        continue

                    _d = dict()
                    _d["_id"], _d["_type"] = d.get("_id"), d.get("_type")
                    _d["ci_type"] = d.get("ci_type")
                    if unique_required:
                        _d[d.get('unique')] = d.get(d.get('unique'))

                    _fields = list(fields.get(_d['_type']) or [] if isinstance(fields, dict) else fields)
                    for field in _fields + ['ci_type_alias', 'unique', 'unique_alias']:
                        _d[field] = d.get(field)
                    _res.append(_d)
                return _res
            else:
                excludes = set(excludes)
                for i in res:
                    for e in excludes:
                        i.pop(e, None)

                return res

    @staticmethod
    def _get_cis_from_db(ci_ids, ret_key=RetKey.NAME, fields=None, value_tables=None, excludes=None):
        from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_IDS
        from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_VALUE_TABLE

        filter_fields_sql = ""
        if fields and isinstance(fields, list):
            _fields = list()
            for field in fields:
                attr = AttributeCache.get(field)
                if attr is not None and not attr.is_password:
                    _fields.append(str(attr.id))
            filter_fields_sql = "WHERE A.attr_id in ({0})".format(",".join(_fields))

        ci2pos = {int(_id): _pos for _pos, _id in enumerate(ci_ids)}
        res = [None] * len(ci_ids)

        ci_ids = ",".join(map(str, ci_ids))
        if value_tables is None:
            value_tables = ValueTypeMap.table_name.values()

        value_sql = " UNION ".join([QUERY_CIS_BY_VALUE_TABLE.format(value_table, ci_ids)
                                    for value_table in value_tables])
        query_sql = QUERY_CIS_BY_IDS.format(filter_fields_sql, value_sql)
        # current_app.logger.debug(query_sql)
        cis = db.session.execute(query_sql).fetchall()
        ci_set = set()
        ci_dict = dict()
        unique_id2obj = dict()
        excludes = excludes and set(excludes)
        for ci_id, type_id, attr_id, attr_name, attr_alias, value, value_type, is_list, is_password in cis:
            if not fields and excludes and (attr_name in excludes or attr_alias in excludes):
                continue

            if ci_id not in ci_set:
                ci_dict = dict()
                ci_type = CITypeCache.get(type_id)
                ci_dict["_id"] = ci_id
                ci_dict["_type"] = type_id
                ci_dict["ci_type"] = ci_type.name
                ci_dict["ci_type_alias"] = ci_type.alias
                if ci_type.unique_id not in unique_id2obj:
                    unique_id2obj[ci_type.unique_id] = AttributeCache.get(ci_type.unique_id)
                ci_dict["unique"] = unique_id2obj[ci_type.unique_id] and unique_id2obj[ci_type.unique_id].name
                ci_dict["unique_alias"] = unique_id2obj[ci_type.unique_id] and unique_id2obj[ci_type.unique_id].alias
                ci_set.add(ci_id)
                res[ci2pos[ci_id]] = ci_dict

            if isinstance(fields, dict) and fields.get(type_id):
                if attr_name not in fields[type_id]:
                    continue

            if ret_key == RetKey.NAME:
                attr_key = attr_name
            elif ret_key == RetKey.ALIAS:
                attr_key = attr_alias
            elif ret_key == RetKey.ID:
                attr_key = attr_id
            else:
                return abort(400, ErrFormat.argument_invalid.format("ret_key"))

            if is_password and value:
                ci_dict[attr_key] = PASSWORD_DEFAULT_SHOW
            else:
                value = ValueTypeMap.serialize2[value_type](value)
                if is_list:
                    ci_dict.setdefault(attr_key, []).append(value)
                else:
                    ci_dict[attr_key] = value

        return res

    @classmethod
    def get_cis_by_ids(cls, ci_ids, ret_key=RetKey.NAME,
                       fields=None, value_tables=None, unique_required=False, excludes=None):
        """

        :param ci_ids: list of CI instance ID, e.g. ['1', '2']
        :param ret_key: name, id or alias
        :param fields:
        :param value_tables:
        :param unique_required:
        :param excludes: exclude field list
        :return:
        """

        if not ci_ids:
            return []

        fields = [] if not fields else fields

        ci_id_tuple = tuple(map(int, ci_ids))
        res = cls._get_cis_from_cache(ci_id_tuple, ret_key, fields, unique_required, excludes=excludes)
        if res is not None:
            return res

        current_app.logger.warning("cache not hit...............")

        return cls._get_cis_from_db(ci_ids, ret_key, fields, value_tables, excludes=excludes)

    @classmethod
    def save_password(cls, ci_id, attr_id, value, record_id, type_id):
        value, is_dynamic = value
        changed = None
        encrypt_value = None
        value_table = ValueTypeMap.table[ValueTypeEnum.PASSWORD]
        if current_app.config.get('SECRETS_ENGINE') == 'inner':
            if value:
                encrypt_value, status = InnerCrypt().encrypt(str(value))
                if not status:
                    current_app.logger.error('save password failed: {}'.format(encrypt_value))
                    return abort(400, ErrFormat.password_save_failed.format(encrypt_value))
        else:
            encrypt_value = PASSWORD_DEFAULT_SHOW

        existed = value_table.get_by(ci_id=ci_id, attr_id=attr_id, first=True, to_dict=False)
        if existed is None:
            if value:
                value_table.create(ci_id=ci_id, attr_id=attr_id, value=encrypt_value)
                if not is_dynamic:
                    changed = [(ci_id, attr_id, OperateType.ADD, '', PASSWORD_DEFAULT_SHOW, type_id)]
        elif existed.value != encrypt_value:
            if value:
                existed.update(ci_id=ci_id, attr_id=attr_id, value=encrypt_value)
                if not is_dynamic:
                    changed = [(ci_id, attr_id, OperateType.UPDATE, PASSWORD_DEFAULT_SHOW,
                                PASSWORD_DEFAULT_SHOW, type_id)]
            else:
                existed.delete()
                if not is_dynamic:
                    changed = [(ci_id, attr_id, OperateType.DELETE, PASSWORD_DEFAULT_SHOW, '', type_id)]

        if current_app.config.get('SECRETS_ENGINE') == 'vault':
            vault = VaultClient(current_app.config.get('VAULT_URL'), current_app.config.get('VAULT_TOKEN'))
            if value:
                try:
                    vault.update("/{}/{}".format(ci_id, attr_id), dict(v=str(value)))
                except Exception as e:
                    current_app.logger.error('save password to vault failed: {}'.format(e))
                    return abort(400, ErrFormat.password_save_failed.format('write vault failed'))
            else:
                try:
                    vault.delete("/{}/{}".format(ci_id, attr_id))
                except Exception as e:
                    current_app.logger.warning('delete password to vault failed: {}'.format(e))

        if changed is not None:
            return AttributeValueManager.write_change2(changed, record_id)

    @classmethod
    def load_password(cls, ci_id, attr_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format(ci_id))

        limit_attrs = cls._valid_ci_for_no_read(ci, ci.ci_type)
        if limit_attrs:
            attr = AttributeCache.get(attr_id)
            if attr and attr.name not in limit_attrs:
                return abort(403, ErrFormat.no_permission2)

        if current_app.config.get('SECRETS_ENGINE', 'inner') == 'inner':
            value_table = ValueTypeMap.table[ValueTypeEnum.PASSWORD]
            v = value_table.get_by(ci_id=ci_id, attr_id=attr_id, first=True, to_dict=False)

            v = v and v.value
            if not v:
                return

            decrypt_value, status = InnerCrypt().decrypt(v)
            if not status:
                current_app.logger.error('load password failed: {}'.format(decrypt_value))
                return abort(400, ErrFormat.password_load_failed.format(decrypt_value))

            return decrypt_value

        elif current_app.config.get('SECRETS_ENGINE') == 'vault':
            vault = VaultClient(current_app.config.get('VAULT_URL'), current_app.config.get('VAULT_TOKEN'))
            data, status = vault.read("/{}/{}".format(ci_id, attr_id))
            if not status:
                current_app.logger.error('read password from vault failed: {}'.format(data))
                return abort(400, ErrFormat.password_load_failed.format(data))

            return data.get('v')

    def baseline(self, ci_ids, before_date):
        """
        return CI changes
        :param ci_ids:
        :param before_date:
        :return:
        """
        ci_list = self.get_cis_by_ids(ci_ids, ret_key=RetKey.ALIAS)
        if not ci_list:
            return dict()

        ci2changed = dict()
        changed = AttributeHistoryManger.get_records_for_attributes(
            before_date, None, None, 1, 100000, None, None, ci_ids=ci_ids, more=True)[1]
        for records in changed:
            for change in records[1]:
                if change['is_computed'] or change['is_password']:
                    continue

                if change.get('default') and change['default'].get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                    continue

                ci2changed.setdefault(change['ci_id'], {})
                item = (change['old'],
                        change['new'],
                        change.get('is_list'),
                        change.get('value_type'),
                        change['operate_type'])
                if change.get('is_list'):
                    ci2changed[change['ci_id']].setdefault(change.get('attr_alias'), []).append(item)
                else:
                    ci2changed[change['ci_id']].update({change.get('attr_alias'): item})

        type2show_name = {}
        result = []
        for ci in ci_list:
            list_attr2item = {}
            for alias_name, v in (ci2changed.get(ci['_id']) or {}).items():
                if not alias_name:
                    continue
                if alias_name == ci.get('unique_alias'):
                    continue

                if ci.get('_type') not in type2show_name:
                    ci_type = CITypeCache.get(ci.get('_type'))
                    show_id = ci_type.show_id or ci_type.unique_id
                    type2show_name[ci['_type']] = AttributeCache.get(show_id).alias

                if isinstance(v, list):
                    for old, new, is_list, value_type, operate_type in v:
                        if alias_name not in list_attr2item:
                            list_attr2item[alias_name] = dict(instance=ci.get(type2show_name[ci['_type']]),
                                                              attr_name=alias_name,
                                                              value_type=value_type,
                                                              is_list=is_list,
                                                              ci_type=ci.get('ci_type'),
                                                              unique_alias=ci.get('unique_alias'),
                                                              unique_value=ci.get(ci['unique_alias']),
                                                              cur=copy.deepcopy(ci.get(alias_name)),
                                                              to=ci.get(alias_name) or [])

                        old = ValueTypeMap.deserialize[value_type](old) if old else old
                        new = ValueTypeMap.deserialize[value_type](new) if new else new
                        if operate_type == OperateType.ADD:
                            list_attr2item[alias_name]['to'].remove(new)
                        elif operate_type == OperateType.DELETE and old not in list_attr2item[alias_name]['to']:
                            list_attr2item[alias_name]['to'].append(old)
                    continue

                old, value_type = v[0], v[3]
                old = ValueTypeMap.deserialize[value_type](old) if old else old
                if isinstance(old, (datetime.datetime, datetime.date)):
                    old = str(old)
                if ci.get(alias_name) != old:
                    item = dict(instance=ci.get(type2show_name[ci['_type']]),
                                attr_name=alias_name,
                                value_type=value_type,
                                ci_type=ci.get('ci_type'),
                                unique_alias=ci.get('unique_alias'),
                                unique_value=ci.get(ci['unique_alias']),
                                cur=ci.get(alias_name),
                                to=old)
                    result.append(item)

            for alias_name, item in list_attr2item.items():
                if sorted(item['cur'] or []) != sorted(item['to'] or []):
                    result.append(item)

        return result

    def baseline_cis(self, ci_ids, before_date, fl=None):
        """
               return CI changes
               :param ci_ids:
               :param before_date:
               :param fl:
               :return:
               """
        ci_list = self.get_cis_by_ids(ci_ids, fields=fl)
        if not ci_list:
            return []

        id2ci = {ci['_id']: ci for ci in ci_list}
        changed = AttributeHistoryManger.get_records_for_attributes(
            before_date, None, None, 1, 100000, None, None, ci_ids=ci_ids, more=True)[1]
        for records in changed:
            for change in records[1]:
                if change['is_computed'] or change['is_password']:
                    continue

                if change.get('default') and change['default'].get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                    continue

                if change['is_list']:
                    old, new, value_type, operate_type, ci_id, attr_name = (
                        change['old'], change['new'], change['value_type'], change['operate_type'],
                        change['ci_id'], change['attr_name'])
                    old = ValueTypeMap.deserialize[value_type](old) if old else old
                    new = ValueTypeMap.deserialize[value_type](new) if new else new
                    if operate_type == OperateType.ADD and new in (id2ci[ci_id][attr_name] or []):
                        id2ci[ci_id][attr_name].remove(new)
                    elif operate_type == OperateType.DELETE and old not in id2ci[ci_id][attr_name]:
                        id2ci[ci_id][attr_name].append(old)
                else:
                    id2ci[change['ci_id']][change['attr_name']] = change['old']

        return list(id2ci.values())

    def rollback(self, ci_id, before_date):
        baseline_ci = self.baseline([ci_id], before_date)

        payload = dict()
        for item in baseline_ci:
            payload[item.get('attr_name')] = item.get('to')

        if payload:
            payload['ci_type'] = baseline_ci[0]['ci_type']
            payload[baseline_ci[0]['unique_alias']] = baseline_ci[0]['unique_value']

            self.update(ci_id, **payload)

        return payload


class CIRelationManager(object):
    """
    Manage relation between CIs
    """

    def __init__(self):
        pass

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

    @staticmethod
    def get_second_cis(first_ci_id, relation_type_id=None, page=1, per_page=None):
        second_cis = db.session.query(CI.id).filter(CI.deleted.is_(False)).join(
            CIRelation, CIRelation.second_ci_id == CI.id).filter(
            CIRelation.first_ci_id == first_ci_id).filter(CIRelation.deleted.is_(False))

        if relation_type_id is not None:
            second_cis = second_cis.filter(CIRelation.relation_type_id == relation_type_id)

        numfound = second_cis.count()
        if per_page != "all":
            second_cis = second_cis.offset((page - 1) * per_page).limit(per_page).all()
        ci_ids = [str(son.id) for son in second_cis]
        result = CIManager.get_cis_by_ids(ci_ids)

        return numfound, len(ci_ids), result

    @staticmethod
    def recursive_children(ci_id):
        result = []

        def _get_children(_id):
            children = CIRelation.get_by(first_ci_id=_id, to_dict=False)
            result.extend([i.second_ci_id for i in children])
            for child in children:
                _get_children(child.second_ci_id)

        _get_children(ci_id)

        return result

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
    def get_ancestor_ids(cls, ci_ids, level=1):
        level2ids = dict()
        for _level in range(1, level + 1):
            cis = db.session.query(CIRelation.first_ci_id, CIRelation.ancestor_ids).filter(
                CIRelation.second_ci_id.in_(ci_ids)).filter(CIRelation.deleted.is_(False))
            ci_ids = [i.first_ci_id for i in cis]
            level2ids[_level + 1] = {int(i.ancestor_ids.split(',')[-1]) for i in cis if i.ancestor_ids}

        return ci_ids, level2ids

    @classmethod
    def get_parent_ids(cls, ci_ids):
        cis = db.session.query(CIRelation.first_ci_id, CIRelation.second_ci_id, CI.type_id).join(
            CI, CI.id == CIRelation.first_ci_id).filter(
            CIRelation.second_ci_id.in_(ci_ids)).filter(CIRelation.deleted.is_(False))

        result = {}
        for ci in cis:
            result.setdefault(ci.second_ci_id, []).append((ci.first_ci_id, ci.type_id))

        return result

    @staticmethod
    def _check_constraint(first_ci_id, first_type_id, second_ci_id, second_type_id, type_relation):
        db.session.commit()
        if type_relation.constraint == ConstraintEnum.Many2Many:
            return

        first_existed = CIRelation.get_by(first_ci_id=first_ci_id,
                                          relation_type_id=type_relation.relation_type_id, to_dict=False)
        second_existed = CIRelation.get_by(second_ci_id=second_ci_id,
                                           relation_type_id=type_relation.relation_type_id, to_dict=False)
        if type_relation.constraint == ConstraintEnum.One2One:
            for i in first_existed:
                if i.second_ci.type_id == second_type_id:
                    return abort(400, ErrFormat.relation_constraint.format("1-1"))

            for i in second_existed:
                if i.first_ci.type_id == first_type_id:
                    return abort(400, ErrFormat.relation_constraint.format("1-1"))

        if type_relation.constraint == ConstraintEnum.One2Many:
            for i in second_existed:
                if i.first_ci.type_id == first_type_id:
                    return abort(400, ErrFormat.relation_constraint.format("1-N"))

    @classmethod
    def add(cls, first_ci_id, second_ci_id,
            more=None,
            relation_type_id=None,
            ancestor_ids=None,
            valid=True,
            apply_async=True,
            source=None,
            uid=None):

        first_ci = CIManager.confirm_ci_existed(first_ci_id)
        second_ci = CIManager.confirm_ci_existed(second_ci_id)

        existed = CIRelation.get_by(first_ci_id=first_ci_id,
                                    second_ci_id=second_ci_id,
                                    ancestor_ids=ancestor_ids,
                                    to_dict=False,
                                    first=True)
        if existed is not None:
            if existed.relation_type_id != relation_type_id and relation_type_id is not None:
                source = existed.source or source
                existed.update(relation_type_id=relation_type_id, source=source)

                CIRelationHistoryManager().add(existed, OperateType.UPDATE, uid=uid)
        else:
            if relation_type_id is None:
                type_relation = CITypeRelation.get_by(parent_id=first_ci.type_id,
                                                      child_id=second_ci.type_id,
                                                      first=True,
                                                      to_dict=False)
                relation_type_id = type_relation and type_relation.relation_type_id
                relation_type_id or abort(404, ErrFormat.relation_not_found.format("{} -> {}".format(
                    first_ci.ci_type.name, second_ci.ci_type.name)))

                if current_app.config.get('USE_ACL') and valid and current_user.username != 'worker':
                    resource_name = CITypeRelationManager.acl_resource_name(first_ci.ci_type.name,
                                                                            second_ci.ci_type.name)
                    if not ACLManager().has_permission(
                            resource_name,
                            ResourceTypeEnum.CI_TYPE_RELATION,
                            PermEnum.ADD):
                        return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.ADD))

            else:
                type_relation = CITypeRelation.get_by_id(relation_type_id)

            with redis_lock.Lock(rd.r,
                                 "ci_relation_add_{}_{}".format(first_ci.type_id, second_ci.type_id),
                                 expire=10):

                cls._check_constraint(first_ci_id, first_ci.type_id, second_ci_id, second_ci.type_id, type_relation)

                existed = CIRelation.create(first_ci_id=first_ci_id,
                                            second_ci_id=second_ci_id,
                                            relation_type_id=relation_type_id,
                                            ancestor_ids=ancestor_ids,
                                            source=source)
                CIRelationHistoryManager().add(existed, OperateType.ADD, uid=uid)
                if apply_async:
                    ci_relation_cache.apply_async(args=(first_ci_id, second_ci_id, ancestor_ids), queue=CMDB_QUEUE)
                else:
                    ci_relation_cache(first_ci_id, second_ci_id, ancestor_ids)

        if more is not None:
            existed.upadte(more=more)

        return existed.id

    @staticmethod
    def delete(cr_id, apply_async=True, valid=True):
        cr = CIRelation.get_by_id(cr_id) or abort(404, ErrFormat.relation_not_found.format("id={}".format(cr_id)))

        if current_app.config.get('USE_ACL') and current_user.username != 'worker' and valid:
            resource_name = CITypeRelationManager.acl_resource_name(cr.first_ci.ci_type.name, cr.second_ci.ci_type.name)
            if not ACLManager().has_permission(
                    resource_name,
                    ResourceTypeEnum.CI_TYPE_RELATION,
                    PermEnum.DELETE):
                return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.DELETE))

        cr.delete()

        his_manager = CIRelationHistoryManager()
        his_manager.add(cr, operate_type=OperateType.DELETE)

        if apply_async:
            ci_relation_delete.apply_async(args=(cr.first_ci_id, cr.second_ci_id, cr.ancestor_ids), queue=CMDB_QUEUE)
            delete_id_filter.apply_async(args=(cr.second_ci_id,), queue=CMDB_QUEUE)
        else:
            ci_relation_delete(cr.first_ci_id, cr.second_ci_id, cr.ancestor_ids)
            delete_id_filter(cr.second_ci_id)

        return cr_id

    @classmethod
    def delete_2(cls, first_ci_id, second_ci_id, ancestor_ids=None):
        cr = CIRelation.get_by(first_ci_id=first_ci_id,
                               second_ci_id=second_ci_id,
                               ancestor_ids=ancestor_ids,
                               to_dict=False,
                               first=True)

        if cr is not None:
            cls.delete(cr.id)

        # ci_relation_delete.apply_async(args=(first_ci_id, second_ci_id, ancestor_ids), queue=CMDB_QUEUE)
        # delete_id_filter.apply_async(args=(second_ci_id,), queue=CMDB_QUEUE)

        return cr

    @classmethod
    def delete_3(cls, first_ci_id, second_ci_id, apply_async=True, valid=True):
        cr = CIRelation.get_by(first_ci_id=first_ci_id,
                               second_ci_id=second_ci_id,
                               to_dict=False,
                               first=True)

        if cr is not None:
            # ci_relation_delete.apply_async(args=(first_ci_id, second_ci_id, cr.ancestor_ids), queue=CMDB_QUEUE)
            # delete_id_filter.apply_async(args=(second_ci_id,), queue=CMDB_QUEUE)

            cls.delete(cr.id, apply_async=apply_async, valid=valid)

        return cr

    @classmethod
    def batch_update(cls, ci_ids, parents, children, ancestor_ids=None):
        """
        only for many to one
        :param ci_ids:
        :param parents:
        :param children:
        :param ancestor_ids:
        :return:
        """
        if isinstance(parents, list):
            for parent_id in parents:
                for ci_id in ci_ids:
                    cls.add(parent_id, ci_id, ancestor_ids=ancestor_ids)

        if isinstance(children, list):
            for child_id in children:
                for ci_id in ci_ids:
                    cls.add(ci_id, child_id, ancestor_ids=ancestor_ids)

    @classmethod
    def batch_delete(cls, ci_ids, parents, ancestor_ids=None):
        """
        only for many to one
        :param ci_ids:
        :param parents:
        :param ancestor_ids:
        :return:
        """

        if isinstance(parents, list):
            for parent_id in parents:
                for ci_id in ci_ids:
                    cls.delete_2(parent_id, ci_id, ancestor_ids=ancestor_ids)

    @classmethod
    def delete_relations_by_source(cls, source,
                                   first_ci_id=None, second_ci_type_id=None,
                                   second_ci_id=None, first_ci_type_id=None,
                                   added=None):
        existed = []
        if first_ci_id is not None and second_ci_type_id is not None:
            existed = [(i.first_ci_id, i.second_ci_id) for i in CIRelation.get_by(
                source=source, first_ci_id=first_ci_id, only_query=True).join(
                CI, CIRelation.second_ci_id == CI.id).filter(CI.type_id == second_ci_type_id)]

        if second_ci_id is not None and first_ci_type_id is not None:
            existed = [(i.first_ci_id, i.second_ci_id) for i in CIRelation.get_by(
                source=source, second_ci_id=second_ci_id, only_query=True).join(
                CI, CIRelation.first_ci_id == CI.id).filter(CI.type_id == first_ci_type_id)]

        deleted = set(existed) - set(added or [])

        for first, second in deleted:
            cls.delete_3(first, second, apply_async=False)

    @classmethod
    def build_by_attribute(cls, ci_dict):
        type_id = ci_dict['_type']
        child_items = CITypeRelation.get_by(parent_id=type_id, only_query=True).filter(
            CITypeRelation.parent_attr_ids.isnot(None))
        for item in child_items:
            relations = None
            for parent_attr_id, child_attr_id in zip(item.parent_attr_ids, item.child_attr_ids):
                _relations = set()
                parent_attr = AttributeCache.get(parent_attr_id)
                child_attr = AttributeCache.get(child_attr_id)
                attr_value = ci_dict.get(parent_attr.name)
                if attr_value != 0 and not attr_value:
                    continue
                value_table = TableMap(attr=child_attr).table
                attr_value_list = [attr_value] if not isinstance(attr_value, list) else attr_value

                matching_cis = value_table.get_by(
                    attr_id=child_attr.id,
                    only_query=True
                ).join(
                    CI, CI.id == value_table.ci_id
                ).filter(
                    CI.type_id == item.child_id,
                    value_table.value.in_(attr_value_list)
                ).all()

                for ci in matching_cis:
                    _relations.add((ci_dict['_id'], ci.ci_id))

                if relations is None:
                    relations = _relations
                else:
                    if item.constraint == ConstraintEnum.Many2Many:
                        relations |= _relations
                    else:
                        relations &= _relations

            cls.delete_relations_by_source(RelationSourceEnum.ATTRIBUTE_VALUES,
                                           first_ci_id=ci_dict['_id'],
                                           second_ci_type_id=item.child_id,
                                           added=relations)
            for parent_ci_id, child_ci_id in (relations or []):
                cls.add(parent_ci_id, child_ci_id,
                        valid=False,
                        source=RelationSourceEnum.ATTRIBUTE_VALUES)

        parent_items = CITypeRelation.get_by(child_id=type_id, only_query=True).filter(
            CITypeRelation.child_attr_ids.isnot(None))
        for item in parent_items:
            relations = None
            for parent_attr_id, child_attr_id in zip(item.parent_attr_ids, item.child_attr_ids):
                _relations = set()
                parent_attr = AttributeCache.get(parent_attr_id)
                child_attr = AttributeCache.get(child_attr_id)
                attr_value = ci_dict.get(child_attr.name)
                if attr_value != 0 and not attr_value:
                    continue
                value_table = TableMap(attr=parent_attr).table
                attr_value_list = [attr_value] if not isinstance(attr_value, list) else attr_value

                matching_cis = value_table.get_by(
                    attr_id=parent_attr.id,
                    only_query=True
                ).join(
                    CI, CI.id == value_table.ci_id
                ).filter(
                    CI.type_id == item.parent_id,
                    value_table.value.in_(attr_value_list)
                ).all()

                for ci in matching_cis:
                    _relations.add((ci.ci_id, ci_dict['_id']))

                if relations is None:
                    relations = _relations
                else:
                    if item.constraint == ConstraintEnum.Many2Many:
                        relations |= _relations
                    else:
                        relations &= _relations

            cls.delete_relations_by_source(RelationSourceEnum.ATTRIBUTE_VALUES,
                                           second_ci_id=ci_dict['_id'],
                                           first_ci_type_id=item.parent_id,
                                           added=relations)
            for parent_ci_id, child_ci_id in (relations or []):
                cls.add(parent_ci_id, child_ci_id,
                        valid=False,
                        source=RelationSourceEnum.ATTRIBUTE_VALUES)

    @classmethod
    def rebuild_all_by_attribute(cls, ci_type_relation, uid):
        relations = None
        for parent_attr_id, child_attr_id in zip(ci_type_relation['parent_attr_ids'] or [],
                                                 ci_type_relation['child_attr_ids'] or []):

            _relations = set()
            parent_attr = AttributeCache.get(parent_attr_id)
            child_attr = AttributeCache.get(child_attr_id)
            if not parent_attr or not child_attr:
                continue

            parent_value_table = TableMap(attr=parent_attr).table
            child_value_table = TableMap(attr=child_attr).table

            parent_values = parent_value_table.get_by(attr_id=parent_attr.id, only_query=True).join(
                CI, CI.id == parent_value_table.ci_id).filter(CI.type_id == ci_type_relation['parent_id'])
            child_values = child_value_table.get_by(attr_id=child_attr.id, only_query=True).join(
                CI, CI.id == child_value_table.ci_id).filter(CI.type_id == ci_type_relation['child_id'])

            child_value2ci_ids = {}
            for child in child_values:
                child_value2ci_ids.setdefault(child.value, []).append(child.ci_id)

            for parent in parent_values:
                for child_ci_id in child_value2ci_ids.get(parent.value, []):
                    _relations.add((parent.ci_id, child_ci_id))

            if relations is None:
                relations = _relations
            else:
                relations &= _relations

        t1 = aliased(CI)
        t2 = aliased(CI)
        query = db.session.query(CIRelation).join(t1, t1.id == CIRelation.first_ci_id).join(
            t2, t2.id == CIRelation.second_ci_id).filter(t1.type_id == ci_type_relation['parent_id']).filter(
            t2.type_id == ci_type_relation['child_id'])
        for i in query:
            db.session.delete(i)
            ci_relation_delete(i.first_ci_id, i.second_ci_id, i.ancestor_ids)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()

        for parent_ci_id, child_ci_id in (relations or []):
            try:
                cls.add(parent_ci_id, child_ci_id,
                        valid=False,
                        apply_async=False,
                        source=RelationSourceEnum.ATTRIBUTE_VALUES,
                        uid=uid)
            except Exception as e:
                current_app.logger.error(e)


class CITriggerManager(object):
    @staticmethod
    def get(type_id):
        db.session.commit()
        return CITypeTrigger.get_by(type_id=type_id, to_dict=True)

    @staticmethod
    def _update_old_attr_value(record_id, ci_dict):
        attr_history = AttributeHistory.get_by(record_id=record_id, to_dict=False)
        attr_dict = dict()
        for attr_h in attr_history:
            attr_dict['old_{}'.format(AttributeCache.get(attr_h.attr_id).name)] = attr_h.old

        ci_dict.update({'old_{}'.format(k): ci_dict[k] for k in ci_dict})

        ci_dict.update(attr_dict)

    @classmethod
    def _exec_webhook(cls, operate_type, webhook, ci_dict, trigger_id, trigger_name, record_id,
                      ci_id=None, app=None, record_history=True):
        app = app or current_app

        with app.app_context():
            if operate_type == OperateType.UPDATE:
                cls._update_old_attr_value(record_id, ci_dict)

            if ci_id is not None:
                ci_dict = CIManager().get_ci_by_id_from_db(
                    ci_id, need_children=False, use_master=False, enum_use_label=True)

            try:
                response = webhook_request(webhook, ci_dict)
                response.raise_for_status()
                is_ok = True
            except Exception as e:
                current_app.logger.warning("exec webhook failed: {}".format(e))
                response = e
                is_ok = False
            if record_history:
                CITriggerHistoryManager.add(operate_type,
                                            record_id,
                                            ci_dict.get('_id'),
                                            trigger_id,
                                            trigger_name,
                                            is_ok=is_ok,
                                            webhook=response)

            return is_ok

    @classmethod
    def _exec_notify(cls, operate_type, notify, ci_dict, trigger_id, trigger_name, record_id,
                     ci_id=None, app=None, record_history=True):
        app = app or current_app

        with app.app_context():

            if ci_id is not None:
                ci_dict = CIManager().get_ci_by_id_from_db(
                    ci_id, need_children=False, use_master=False, enum_use_label=True)

            if operate_type == OperateType.UPDATE:
                cls._update_old_attr_value(record_id, ci_dict)

            is_ok = True
            response = ''
            for method in (notify.get('method') or []):
                try:
                    res = notify_send(notify.get('subject'), notify.get('body'), [method],
                                      notify.get('tos'), ci_dict)
                    response = "{}\n{}".format(response, res)
                except Exception as e:
                    current_app.logger.warning("send notify failed: {}".format(e))
                    response = "{}\n{}".format(response, e)
                    is_ok = False

            if record_history:
                CITriggerHistoryManager.add(operate_type,
                                            record_id,
                                            ci_dict.get('_id'),
                                            trigger_id,
                                            trigger_name,
                                            is_ok=is_ok,
                                            notify=response.strip())

            return is_ok

    @staticmethod
    def ci_filter(ci_id, other_filter):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search

        query = "{},_id:{}".format(other_filter, ci_id)

        try:
            _, _, _, _, numfound, _ = search(query).search()
            return numfound
        except SearchError as e:
            current_app.logger.warning("ci search failed: {}".format(e))

    @classmethod
    def fire(cls, operate_type, ci_dict, record_id):
        type_id = ci_dict.get('_type')
        triggers = cls.get(type_id) or []

        for trigger in triggers:
            option = trigger['option']
            if not option.get('enable'):
                continue

            if option.get('filter') and not cls.ci_filter(ci_dict.get('_id'), option['filter']):
                continue

            if option.get('attr_ids') and isinstance(option['attr_ids'], list):
                if not (set(option['attr_ids']) &
                        set([i.attr_id for i in AttributeHistory.get_by(record_id=record_id, to_dict=False)])):
                    continue

            if option.get('action') == operate_type:
                cls.fire_by_trigger(trigger, operate_type, ci_dict, record_id)

    @classmethod
    def fire_by_trigger(cls, trigger, operate_type, ci_dict, record_id=None):
        option = trigger['option']

        if option.get('webhooks'):
            cls._exec_webhook(operate_type, option['webhooks'], ci_dict, trigger['id'],
                              option.get('name'), record_id)

        elif option.get('notifies'):
            cls._exec_notify(operate_type, option['notifies'], ci_dict, trigger['id'],
                             option.get('name'), record_id)

    @classmethod
    def waiting_cis(cls, trigger):
        now = datetime.datetime.today()

        config = trigger.option.get('notifies') or {}

        delta_time = datetime.timedelta(days=(config.get('before_days', 0) or 0))

        attr = AttributeCache.get(trigger.attr_id)

        value_table = TableMap(attr=attr).table

        values = value_table.get_by(attr_id=attr.id, to_dict=False)

        result = []
        for v in values:
            if (isinstance(v.value, (datetime.date, datetime.datetime)) and
                    (v.value - delta_time).strftime('%Y%m%d') == now.strftime("%Y%m%d")):

                if trigger.option.get('filter') and not cls.ci_filter(v.ci_id, trigger.option['filter']):
                    continue

                result.append(v)

        return result

    @classmethod
    def trigger_notify(cls, trigger, ci, only_test=False):
        """
        only for date attribute
        :param trigger:
        :param ci:
        :param only_test:
        :return:
        """
        if (trigger.option.get('notifies', {}).get('notify_at') == datetime.datetime.now().strftime("%H:%M") or
            not trigger.option.get('notifies', {}).get('notify_at')) or only_test:

            if trigger.option.get('webhooks'):
                threading.Thread(
                    target=cls._exec_webhook,
                    args=(None, trigger.option['webhooks'], None, trigger.id,
                          trigger.option.get('name'), None,
                          ci and ci.ci_id,
                          current_app._get_current_object(), not only_test)).start()
            elif trigger.option.get('notifies'):
                threading.Thread(target=cls._exec_notify, args=(
                    None, trigger.option['notifies'], None, trigger.id,
                    trigger.option.get('name'), None,
                    ci and ci.ci_id,
                    current_app._get_current_object(), not only_test)).start()

            return True

        return False

    @classmethod
    def trigger_notify_test(cls, type_id, trigger_id):
        trigger = CITypeTrigger.get_by_id(trigger_id) or abort(
            404, ErrFormat.ci_type_trigger_not_found.format(trigger_id))

        ci_type = CITypeCache.get(type_id) or abort(404, ErrFormat.ci_type_not_found.format(type_id))
        attr = AttributeCache.get(ci_type.unique_id)
        value_table = TableMap(attr=attr).table
        if not value_table:
            return

        value = value_table.get_by(attr_id=attr.id, only_query=True).join(
            CI, value_table.ci_id == CI.id).filter(CI.type_id == type_id).first()

        cls.trigger_notify(trigger, value, only_test=True)
