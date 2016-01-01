# -*- coding:utf-8 -*- 


import datetime

from flask import current_app

from extensions import db
from models.attribute import CIAttributeCache
from lib.attribute import AttributeManager
from lib.const import type_map
from lib.const import TableMap


class AttributeValueManager(object):
    """
    manage CI attribute values
    """

    def __init__(self):
        pass

    def _get_attr(self, key):
        """key is one of attr_id, attr_name and attr_alias
        """
        attr = CIAttributeCache.get(key)
        return attr

    def _get_attr_values(self, fields, ci_id,
                         ret_key="name",
                         uniq_key=None,
                         use_master=False):
        res = dict()
        for field in fields:
            attr = CIAttributeCache.get(field)
            if not attr:
                current_app.logger.warn('attribute %s not found' % field)
                return res
            table = TableMap(attr_name=attr.attr_name).table
            if use_master:
                rs = db.session().using_bind("master").query(
                    table.value).filter_by(ci_id=ci_id).filter_by(
                        attr_id=attr.attr_id)
            else:
                rs = db.session.query(table.value).filter_by(
                    ci_id=ci_id).filter_by(attr_id=attr.attr_id)
            field_name = getattr(attr, "attr_{0}".format(ret_key))
            try:
                if attr.is_multivalue:
                    if attr.value_type == 'datetime':
                        res[field_name] = [datetime.datetime.strftime(
                            x.value, '%Y-%m-%d %H:%M:%S') for x in rs.all()]
                    else:
                        res[field_name] = [x.value for x in rs.all()]
                else:
                    x = rs.first()
                    if x:
                        if attr.value_type == 'datetime':
                            res[field_name] = datetime.datetime.strftime(
                                rs.first().value, '%Y-%m-%d %H:%M:%S')
                        else:
                            res[field_name] = rs.first().value
                    else:
                        res[field_name] = None
            except AttributeError as e:
                current_app.logger.warn("get ci by id error, {0}".format(e))
                if attr.is_multivalue:
                    res[field_name] = list()
                else:
                    res[field_name] = ""
            if uniq_key is not None and attr.attr_id == uniq_key.attr_id \
                    and rs.first() is not None:
                res['unique'] = uniq_key.attr_name
        return res

    def _validate(self, attr, value, table, ci_id):
        converter = type_map.get("converter").get(attr.value_type)
        try:
            v = converter(value)
        except ValueError:
            return False, "attribute value {0} converter fail".format(value)
        if attr.is_choice:
            choice_list = AttributeManager()._get_choice_value(
                attr.attr_id, attr.value_type)
            if v not in choice_list:
                return False, "{0} is not existed in choice values".format(
                    value)
        elif attr.is_uniq:
            old_value = db.session.query(table.attr_id).filter(
                table.attr_id == attr.attr_id).filter(
                    table.value == v).filter(table.ci_id != ci_id).first()
            if old_value is not None:
                return False, "attribute {0} value {1} must be unique".format(
                    attr.attr_name, value)
        return True, v

    def add_attr_value(self, key, value, ci_id, ci_type,
                       _no_attribute_policy="ignore", ci_existed=False):
        """key is one of attr_id, attr_name and attr_alias
        """
        attr = self._get_attr(key)
        if attr is None:
            if _no_attribute_policy == 'ignore':
                return True, None
            if _no_attribute_policy == 'reject':
                return False, 'attribute {0} not exist'.format(key)
        table, old_value, old_value_table = TableMap(
            attr_name=attr.attr_name).table, None, None
        if ci_existed:
            old_value_table = db.session.query(table).filter(
                table.attr_id == attr.attr_id).filter(
                    table.ci_id == ci_id).first()
            if old_value_table is not None:
                old_value = old_value_table.value
        if not value and ci_existed:
            db.session.query(table).filter(
                table.attr_id == attr.attr_id).filter(
                    table.ci_id == ci_id).delete()
            if old_value:
                return True, (attr.attr_id, "delete", old_value, None)
            else:
                return True, None
        elif not value:
            return True, None
        if not attr.is_multivalue:
            ret, res = self._validate(attr, value, table, ci_id)
            if not ret:
                return False, res
            value_table = table()
            if ci_existed:  # for history
                old = db.session.query(table).filter(
                    table.attr_id == attr.attr_id).filter(
                        table.value == value).filter(
                            table.ci_id == ci_id).first()
                if old is not None:
                    return True, None
                elif old_value_table:
                    value_table = old_value_table
            value_table.ci_id = ci_id
            value_table.attr_id = attr.attr_id
            value_table.value = res
            db.session.add(value_table)
        elif attr.is_multivalue:
            if ci_existed:
                db.session.query(table).filter(
                    table.attr_id == attr.attr_id).filter(
                        table.ci_id == ci_id).delete()

            for v in value.strip().split(","):
                ret, res = self._validate(attr, v, table, ci_id)
                if not ret:
                    return False, res
                value_table = table()
                value_table.ci_id = ci_id
                value_table.attr_id = attr.attr_id
                value_table.value = res
                db.session.add(value_table)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "add attribute value is error, {0}".format(str(e)))
            return False, "add attribute value is error, {0}".format(str(e))
        if ci_existed:
            if old_value != value:
                return True, (attr.attr_id, "update", old_value, value)
            else:
                return True, None
        return True, (attr.attr_id, "add", None, value)