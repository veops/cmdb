# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from flask import abort

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.utils import handle_arg_list


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
                res[field_name] = [ValueTypeMap.serialize[attr.value_type](i.value) for i in rs]
            else:
                res[field_name] = ValueTypeMap.serialize[attr.value_type](rs[0].value) if rs else None

            if unique_key is not None and attr.id == unique_key.id and rs:
                res['unique'] = unique_key.name

        return res

    @staticmethod
    def __deserialize_value(value_type, value):
        if not value:
            return value
        deserialize = ValueTypeMap.deserialize[value_type]
        try:
            v = deserialize(value)
            return v
        except ValueError:
            return abort(400, "attribute value <{0}> is invalid".format(value))

    @staticmethod
    def __check_is_choice(attr, value_type, value):
        choice_values = AttributeManager.get_choice_values(attr.id, value_type)
        if value not in choice_values:
            return abort(400, "{0} does not existed in choice values".format(value))

    @staticmethod
    def __check_is_unique(value_table, attr, ci_id, value):
        existed = db.session.query(value_table.attr_id).filter(
            value_table.attr_id == attr.id).filter(value_table.deleted.is_(False)).filter(
            value_table.value == value).filter(value_table.ci_id != ci_id).first()
        existed and abort(400, "attribute <{0}> value {1} must be unique".format(attr.alias, value))

    @staticmethod
    def __check_is_required(type_id, attr, value):
        type_attr = CITypeAttributeCache.get(type_id, attr.id)
        if type_attr and type_attr.is_required and not value and value != 0:
            return abort(400, "attribute <{0}> value is required".format(attr.alias))

    def _validate(self, attr, value, value_table, ci):
        v = self.__deserialize_value(attr.value_type, value)

        attr.is_choice and value and self.__check_is_choice(attr, attr.value_type, v)
        attr.is_unique and self.__check_is_unique(value_table, attr, ci.id, v)

        self.__check_is_required(ci.type_id, attr, v)

        return v

    @staticmethod
    def _write_change(ci_id, attr_id, operate_type, old, new):
        AttributeHistoryManger.add(ci_id, [(attr_id, operate_type, old, new)])

    def create_or_update_attr_value(self, key, value, ci, _no_attribute_policy=ExistPolicy.IGNORE):
        """
        add or update attribute value, then write history
        :param key: id, name or alias
        :param value:
        :param ci: instance object
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

        if attr.is_list:
            value_list = [self._validate(attr, i, value_table, ci) for i in handle_arg_list(value)]
            if not value_list:
                self.__check_is_required(ci.type_id, attr, '')

            existed_attrs = value_table.get_by(attr_id=attr.id,
                                               ci_id=ci.id,
                                               to_dict=False)
            existed_values = [i.value for i in existed_attrs]
            added = set(value_list) - set(existed_values)
            deleted = set(existed_values) - set(value_list)
            for v in added:
                value_table.create(ci_id=ci.id, attr_id=attr.id, value=v)
                self._write_change(ci.id, attr.id, OperateType.ADD, None, v)

            for v in deleted:
                existed_attr = existed_attrs[existed_values.index(v)]
                existed_attr.delete()
                self._write_change(ci.id, attr.id, OperateType.DELETE, v, None)
        else:
            value = self._validate(attr, value, value_table, ci)
            existed_attr = value_table.get_by(attr_id=attr.id,
                                              ci_id=ci.id,
                                              first=True,
                                              to_dict=False)
            existed_value = existed_attr and existed_attr.value
            if existed_value is None:
                value_table.create(ci_id=ci.id, attr_id=attr.id, value=value)

                self._write_change(ci.id, attr.id, OperateType.ADD, None, value)
            else:
                if existed_value != value:
                    if value != 0 and not value and attr.value_type != ValueTypeEnum.TEXT:
                        existed_attr.delete()
                    else:
                        existed_attr.update(value=value)

                    self._write_change(ci.id, attr.id, OperateType.UPDATE, existed_value, value)

    @staticmethod
    def delete_attr_value(attr_id, ci_id):
        attr = AttributeCache.get(attr_id)
        if attr is not None:
            value_table = TableMap(attr_name=attr.name).table
            for item in value_table.get_by(attr_id=attr.id, ci_id=ci_id, to_dict=False):
                item.delete()
