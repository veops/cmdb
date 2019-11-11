# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

import markupsafe
from flask import abort

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import TableMap
from api.lib.cmdb.const import type_map
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.utils import handle_arg_list
from api.models.cmdb import Attribute


class AttributeValueManager(object):
    """
    manage CI attribute values
    """

    def __init__(self):
        pass

    @staticmethod
    def _get_attr(key):
        """
        :param key: id, name or alias
        :return: attribute instance
        """
        return AttributeCache.get(key)

    def get_attr_values(self, fields, ci_id, ret_key="name", unique_key=None, use_master=False):
        """

        :param fields:
        :param ci_id:
        :param ret_key: It can be name or alias
        :param unique_key: primary attribute
        :param use_master: Only for master-slave read-write separation
        :return:
        """
        res = dict()
        for field in fields:
            attr = self._get_attr(field)
            if not attr:
                continue

            value_table = TableMap(attr_name=attr.name).table
            rs = value_table.get_by(ci_id=ci_id,
                                    attr_id=attr.id,
                                    use_master=use_master,
                                    to_dict=False)
            field_name = getattr(attr, ret_key)

            if attr.is_list:
                res[field_name] = [type_map["serialize"][attr.value_type](i.value) for i in rs]
            else:
                res[field_name] = type_map["serialize"][attr.value_type](rs[0].value) if rs else None

            if unique_key is not None and attr.id == unique_key.id and rs:
                res['unique'] = unique_key.name

        return res

    @staticmethod
    def __deserialize_value(value_type, value):
        if not value:
            return value
        deserialize = type_map["deserialize"][value_type]
        try:
            v = deserialize(value)
            return v
        except ValueError:
            return abort(400, "attribute value <{0}> is invalid".format(value))

    @staticmethod
    def __check_is_choice(attr_id, value_type, value):
        choice_values = AttributeManager.get_choice_values(attr_id, value_type)
        if value not in choice_values:
            return abort(400, "{0} does not existed in choice values".format(value))

    @staticmethod
    def __check_is_unique(value_table, attr_id, ci_id, value):
        existed = db.session.query(value_table.attr_id).filter(
            value_table.attr_id == attr_id).filter(value_table.deleted.is_(False)).filter(
            value_table.value == value).filter(value_table.ci_id != ci_id).first()
        existed and abort(400, "attribute <{0}> value {1} must be unique".format(attr_id, value))

    def _validate(self, attr, value, value_table, ci_id):
        v = self.__deserialize_value(attr.value_type, value)

        attr.is_choice and value and self.__check_is_choice(attr.id, attr.value_type, v)
        attr.is_unique and self.__check_is_unique(value_table, attr.id, ci_id, v)

        return v

    @staticmethod
    def _write_change(ci_id, attr_id, operate_type, old, new):
        AttributeHistoryManger.add(ci_id, [(attr_id, operate_type, old, new)])

    def create_or_update_attr_value(self, key, value, ci_id, _no_attribute_policy=ExistPolicy.IGNORE):
        """
        add or update attribute value, then write history
        :param key: id, name or alias
        :param value:
        :param ci_id:
        :param _no_attribute_policy: ignore or reject
        :return:
        """
        attr = self._get_attr(key)
        if attr is None:
            if _no_attribute_policy == ExistPolicy.IGNORE:
                return
            if _no_attribute_policy == ExistPolicy.REJECT:
                return abort(400, 'attribute {0} does not exist'.format(key))

        value_table = TableMap(attr_name=attr.name).table
        existed_attr = value_table.get_by(attr_id=attr.id,
                                          ci_id=ci_id,
                                          first=True,
                                          to_dict=False)
        existed_value = existed_attr and existed_attr.value
        operate_type = OperateType.ADD if existed_attr is None else OperateType.UPDATE

        value_list = handle_arg_list(value) if attr.is_list else [value]
        if not isinstance(value, list):
            value_list = [value]

        for v in value_list:
            v = self._validate(attr, v, value_table, ci_id)
            if not v and attr.value_type != Attribute.TEXT:
                v = None

            if operate_type == OperateType.ADD:
                if v is not None:
                    value_table.create(ci_id=ci_id, attr_id=attr.id, value=v)
                    self._write_change(ci_id, attr.id, operate_type, None, v)
            elif existed_attr.value != v:
                if v is not None:
                    existed_attr.update(value=v)
                else:
                    existed_attr.delete()
                self._write_change(ci_id, attr.id, operate_type, existed_value, v)
