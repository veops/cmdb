# -*- coding:utf-8 -*- 

from flask import current_app
from flask import abort

from extensions import db
from models.attribute import CIAttribute
from models.attribute import CIAttributeCache
from models import row2dict
from lib.const import type_map


class AttributeManager(object):
    """
    CI attributes manager
    """

    def __init__(self):
        pass

    def _get_choice_value(self, attr_id, value_type):
        _table = type_map.get("choice").get(value_type)
        choice_values = db.session.query(_table.value).filter(
            _table.attr_id == attr_id).all()
        return [choice_value.value for choice_value in choice_values]

    def _add_choice_value(self, choice_value, attr_id, value_type):
        _table = type_map.get("choice").get(value_type)
        db.session.query(_table).filter(_table.attr_id == attr_id).delete()
        db.session.flush()
        for v in choice_value.strip().split(","):
            table = _table()
            table.attr_id = attr_id
            table.value = v
            db.session.add(table)
        db.session.flush()

    def get_attributes(self, name=None):
        """
        return attribute by name,
        if name is None, then return all attributes
        """
        attrs = db.session.query(CIAttribute).filter(
            CIAttribute.attr_name.ilike("%{0}%".format(name))).all() \
            if name is not None else db.session.query(CIAttribute).all()
        res = list()
        for attr in attrs:
            attr_dict = row2dict(attr)
            if attr.is_choice:
                attr_dict["choice_value"] = self._get_choice_value(
                    attr.attr_id, attr.value_type)
            res.append(attr_dict)
        return res

    def get_attribute_by_name(self, attr_name):
        attr = db.session.query(CIAttribute).filter(
            CIAttribute.attr_name == attr_name).first()
        if attr:
            attr_dict = row2dict(attr)
            if attr.is_choice:
                attr_dict["choice_value"] = self._get_choice_value(
                    attr.attr_id, attr.value_type)
            return attr_dict

    def get_attribute_by_alias(self, attr_alias):
        attr = db.session.query(CIAttribute).filter(
            CIAttribute.attr_alias == attr_alias).first()
        if attr:
            attr_dict = row2dict(attr)
            if attr.is_choice:
                attr_dict["choice_value"] = self._get_choice_value(
                    attr.attr_id, attr.value_type)
            return attr_dict

    def get_attribute_by_id(self, attr_id):
        attr = db.session.query(CIAttribute).filter(
            CIAttribute.attr_id == attr_id).first()
        if attr:
            attr_dict = row2dict(attr)
            if attr.is_choice:
                attr_dict["choice_value"] = self._get_choice_value(
                    attr.attr_id, attr.value_type)
            return attr_dict

    def add(self, attr_name, attr_alias, **kwargs):
        choice_value = kwargs.get("choice_value", False)
        attr = CIAttributeCache.get(attr_name)
        if attr is not None:
            return False, "attribute {0} is already existed".format(attr_name)
        is_choice = False
        if choice_value:
            is_choice = True
        if not attr_alias:
            attr_alias = attr_name
        attr = CIAttribute()
        attr.attr_name = attr_name
        attr.attr_alias = attr_alias
        attr.is_choice = is_choice
        attr.is_multivalue = kwargs.get("is_multivalue", False)
        attr.is_uniq = kwargs.get("is_uniq", False)
        attr.is_index = kwargs.get("is_index", False)
        attr.value_type = kwargs.get("value_type", "text")
        db.session.add(attr)
        db.session.flush()

        if choice_value:
            self._add_choice_value(choice_value, attr.attr_id, attr.value_type)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("add attribute error, {0}".format(str(e)))
            return False, str(e)
        CIAttributeCache.clean(attr)
        return True, attr.attr_id

    def update(self, attr_id, *args, **kwargs):
        attr = db.session.query(CIAttribute).filter_by(attr_id=attr_id).first()
        if not attr:
            return False, "CI attribute you want to update is not existed"
        choice_value = kwargs.get("choice_value", False)
        is_choice = False
        if choice_value:
            is_choice = True
        attr.attr_name = args[0]
        attr.attr_alias = args[1]
        if not args[1]:
            attr.attr_alias = args[0]
        attr.is_choice = is_choice
        attr.is_multivalue = kwargs.get("is_multivalue", False)
        attr.is_uniq = kwargs.get("is_uniq", False)
        attr.value_type = kwargs.get("value_type", "text")
        db.session.add(attr)
        db.session.flush()
        if is_choice:
            self._add_choice_value(choice_value, attr.attr_id, attr.value_type)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("update attribute error, {0}".format(
                str(e)))
            return False, str(e)
        CIAttributeCache.clean(attr)
        return True, attr.attr_id

    def delete(self, attr_id):
        attr, name = db.session.query(CIAttribute).filter_by(
            attr_id=attr_id).first(), None
        if attr:
            if attr.is_choice:
                choice_table = type_map["choice"].get(attr.value_type)
                db.session.query(choice_table).filter(
                    choice_table.attr_id == attr_id).delete()
            name = attr.attr_name
            CIAttributeCache.clean(attr)
            db.session.delete(attr)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error("delete attribute error, {0}".format(
                    str(e)))
                return abort(500, str(e))
        else:
            return abort(404, "attribute you want to delete is not existed")
        return name