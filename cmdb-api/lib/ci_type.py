# -*- coding:utf-8 -*- 


from flask import current_app
from flask import abort

from extensions import db
from models import row2dict
from models.ci_type import CITypeAttribute
from models.ci_type import CIType
from models.ci_type import CITypeAttributeCache
from models.ci_type import CITypeCache
from models.ci_type_relation import CITypeRelation
from models.attribute import CIAttributeCache
from lib.attribute import AttributeManager


class CITypeAttributeManager(object):
    """
    manage CIType's attributes, include query, add, update, delete
    """

    def __init__(self):
        pass

    def get_attributes_by_type_id(self, type_id):
        attrs = CITypeAttributeCache.get(type_id)
        attr_manager = AttributeManager()
        result = list()
        for attr in attrs:
            attr_dict = attr_manager.get_attribute_by_id(attr.attr_id)
            attr_dict["is_required"] = attr.is_required
            result.append(attr_dict)
        return result

    def add(self, type_id, attr_ids=None, is_required=False):
        """
        add attributes to CIType, attr_ids are list
        """
        if not attr_ids or not isinstance(attr_ids, list):
            return abort(500, "attr_ids must be required")
        ci_type = CITypeCache.get(type_id)
        if ci_type is None:
            return abort(404, "CIType ID({0}) is not existed".format(type_id))
        for attr_id in attr_ids:
            attr = CIAttributeCache.get(attr_id)
            if attr is None:
                return abort(404,
                             "attribute id {0} is not existed".format(attr_id))
            existed = db.session.query(CITypeAttribute.attr_id).filter_by(
                type_id=type_id).filter_by(attr_id=attr_id).first()
            if existed is not None:
                continue
            current_app.logger.debug(attr_id)
            db.session.add(CITypeAttribute(
                type_id=type_id, attr_id=attr_id, is_required=is_required))
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "add attribute to CIType is error, {0}".format(str(e)))
            return abort(
                500, "add attribute to CIType is error, maybe duplicate entry")

        CITypeAttributeCache.clean(type_id)
        return True

    def delete(self, type_id, attr_ids=None):
        """
        delete attributes at CIType, attr_ids are list
        """
        if not attr_ids or not isinstance(attr_ids, list):
            return abort(
                500, "delete attribute of CIType, attr_ids must be required")
        ci_type = CITypeCache.get(type_id)
        if ci_type is None:
            return abort(
                404, "CIType ID({0}) is not existed".format(type_id))
        for attr_id in attr_ids:
            attr = CIAttributeCache.get(attr_id)
            if attr is None:
                return abort(
                    404, "attribute id {0} is not existed".format(attr_id))
            db.session.query(CITypeAttribute).filter_by(
                type_id=type_id).filter_by(attr_id=attr_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "delete attributes of CIType is error, {0}".format(str(e)))
            return abort(500, "delete attributes of CIType is error")
        CITypeAttributeCache.clean(type_id)
        return True


class CITypeManager(object):
    """
    manage CIType
    """

    def __init__(self):
        pass

    def get_citypes(self, type_name=None):
        ci_types = db.session.query(CIType).all() if type_name is None else \
            db.session.query(CIType).filter(
                CIType.type_name.ilike("%{0}%".format(type_name))).all()
        res = list()
        for ci_type in ci_types:
            type_dict = row2dict(ci_type)
            type_dict["uniq_key"] = CIAttributeCache.get(
                type_dict["uniq_id"]).attr_name
            res.append(type_dict)
        return res

    def query(self, _type):
        citype = CITypeCache.get(_type)
        if citype:
            return row2dict(citype)
        return abort(404, "citype is not found")

    def add(self, type_name, type_alias, _id=None, unique=None,
            icon_url="", enabled=True):
        uniq_key = CIAttributeCache.get(_id) or CIAttributeCache.get(unique)
        if uniq_key is None:
            return False, "uniq_key is not existed"
        citype = CITypeCache.get(type_name)
        if citype:
            return False, "this CIType {0} is existed".format(type_name)
        _citype = CIType()
        _citype.type_name = type_name
        _citype.type_alias = type_alias
        _citype.uniq_id = uniq_key.attr_id
        _citype.enabled = enabled
        _citype.icon_url = icon_url
        db.session.add(_citype)
        db.session.flush()
        _citype_attr = CITypeAttribute()
        _citype_attr.attr_id = uniq_key.attr_id
        _citype_attr.type_id = _citype.type_id
        _citype_attr.is_required = True
        db.session.add(_citype_attr)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("add CIType is error, {0}".format(str(e)))
            return False, str(e)
        CITypeCache.clean(type_name)
        return True, _citype.type_id

    def update(self, type_id, type_name, type_alias, _id=None, unique=None,
               icon_url="", enabled=None):
        citype = CITypeCache.get(type_id)
        if citype is None:
            return False, "CIType {0} is not existed".format(type_name)
        uniq_key = CIAttributeCache.get(_id) or CIAttributeCache.get(unique)
        if uniq_key is not None:
            citype.uniq_id = uniq_key.attr_id
            citype_attr = db.session.query(CITypeAttribute).filter(
                CITypeAttribute.type_id == type_id).filter(
                    CITypeAttribute.attr_id == uniq_key.attr_id).first()
            if citype_attr is None:
                citype_attr = CITypeAttribute()
                citype_attr.attr_id = uniq_key.attr_id
                citype_attr.type_id = type_id
            citype_attr.is_required = True
            db.session.add(citype_attr)
        if type_name:
            citype.type_name = type_name
        if type_alias:
            citype.type_alias = type_alias
        if icon_url:
            citype.icon_url = icon_url
        if enabled is not None:
            citype.enabled = enabled
        db.session.add(citype)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("add CIType is error, {0}".format(str(e)))
            return False, str(e)
        CITypeCache.clean(type_id)
        return True, type_id

    def set_enabled(self, type_id, enabled=True):
        citype = CITypeCache.get(type_id)
        if citype is None:
            return abort(404, "CIType[{0}] is not existed".format(type_id))
        citype.enabled = enabled
        db.session.add(citype)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "set CIType enabled is error, {0}".format(str(e)))
            return abort(500, str(e))
        return type_id

    def delete(self, type_id):
        citype = db.session.query(CIType).filter_by(type_id=type_id).first()
        type_name = citype.type_name
        if citype:
            db.session.delete(citype)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(
                    "delete CIType is error, {0}".format(str(e)))
                return abort(500, str(e))
            CITypeCache.clean(type_id)
            return "CIType {0} deleted".format(type_name)
        return abort(404, "CIType is not existed")


class CITypeRelationManager(object):
    """
    manage relation between CITypes
    """

    def __init__(self):
        pass

    @property
    def relation_types(self):
        """ all CIType relation types
        """
        from lib.const import CITYPE_RELATION_TYPES

        return CITYPE_RELATION_TYPES

    def get_children(self, parent_id):
        children = db.session.query(CITypeRelation).filter(
            CITypeRelation.parent_id == parent_id).all()
        result = []
        for child in children:
            ctr_id = child.ctr_id
            citype = CITypeCache.get(child.child_id)
            citype_dict = row2dict(citype)
            citype_dict["ctr_id"] = ctr_id
            manager = CITypeAttributeManager()
            citype_dict["attributes"] = manager.get_attributes_by_type_id(
                citype.type_id)
            citype_dict["relation_type"] = child.relation_type
            result.append(citype_dict)
        return result

    def get_parents(self, child_id):
        parents = db.session.query(CITypeRelation).filter(
            CITypeRelation.child_id == child_id).all()
        result = []
        for parent in parents:
            ctr_id = parent.ctr_id
            citype = CITypeCache.get(parent.parent_id)
            citype_dict = row2dict(citype)
            citype_dict["ctr_id"] = ctr_id
            manager = CITypeAttributeManager()
            citype_dict["attributes"] = manager.get_attributes_by_type_id(
                citype.type_id)
            citype_dict["relation_type"] = parent.relation_type
            result.append(citype_dict)
        return result

    def add(self, parent, child, relation_type="contain"):
        p = CITypeCache.get(parent)
        if p is None:
            return abort(404, "parent {0} is not existed".format(parent))
        c = CITypeCache.get(child)
        if c is None:
            return abort(404, "child {0} is not existed".format(child))
        existed = db.session.query(CITypeRelation.ctr_id).filter_by(
            parent_id=parent).filter_by(child_id=child).first()
        if existed is not None:
            return True, existed.ctr_id
        ctr = CITypeRelation()
        ctr.parent_id = parent
        ctr.child_id = child
        ctr.relation_type = relation_type
        db.session.add(ctr)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "add CITypeRelation is error, {0}".format(str(e)))
            return abort(
                500, "add CITypeRelation is error, {0}".format(str(e)))
        return ctr.ctr_id

    def delete(self, ctr_id):
        ctr = db.session.query(CITypeRelation).filter(
            CITypeRelation.ctr_id == ctr_id).first()
        if ctr:
            db.session.delete(ctr)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(
                    "delete CITypeRelation is error, {0}".format(str(e)))
                return abort(
                    500, "delete CITypeRelation is error, {0}".format(str(e)))
            return True
        return abort(404, "CIType relation is not existed")

    def delete_2(self, parent, child):
        ctr = db.session.query(CITypeRelation).filter(
            CITypeRelation.parent_id == parent).filter(
                CITypeRelation.child_id == child).first()
        return self.delete(ctr.ctr_id)