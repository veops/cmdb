# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from api.extensions import cache
from api.models.cmdb import Attribute
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import RelationType


class AttributeCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        attr = cache.get('Field::Name::{0}'.format(key)) \
            or cache.get('Field::ID::{0}'.format(key)) \
            or cache.get('Field::Alias::{0}'.format(key))

        if attr is None:
            attr = Attribute.get_by(name=key, first=True, to_dict=False) \
                   or Attribute.get_by_id(key) \
                   or Attribute.get_by(alias=key, first=True, to_dict=False)
            if attr is not None:
                cls.set(attr)
        return attr

    @classmethod
    def set(cls, attr):
        cache.set('Field::ID::{0}'.format(attr.id), attr)
        cache.set('Field::Name::{0}'.format(attr.name), attr)
        cache.set('Field::Alias::{0}'.format(attr.alias), attr)

    @classmethod
    def clean(cls, attr):
        cache.delete('Field::ID::{0}'.format(attr.id))
        cache.delete('Field::Name::{0}'.format(attr.name))
        cache.delete('Field::Alias::{0}'.format(attr.alias))


class CITypeCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get("CIType::ID::{0}".format(key)) or \
            cache.get("CIType::Name::{0}".format(key)) or \
            cache.get("CIType::Alias::{0}".format(key))
        if ct is None:
            ct = CIType.get_by(name=key, first=True, to_dict=False) or \
                 CIType.get_by_id(key) or \
                 CIType.get_by(alias=key, first=True, to_dict=False)
            if ct is not None:
                cls.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set("CIType::Name::{0}".format(ct.name), ct)
        cache.set("CIType::ID::{0}".format(ct.id), ct)
        cache.set("CIType::Alias::{0}".format(ct.alias), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete("CIType::Name::{0}".format(ct.name))
            cache.delete("CIType::ID::{0}".format(ct.id))
            cache.delete("CIType::Alias::{0}".format(ct.alias))


class RelationTypeCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get("RelationType::ID::{0}".format(key)) or \
            cache.get("RelationType::Name::{0}".format(key))
        if ct is None:
            ct = RelationType.get_by(name=key, first=True, to_dict=False) or RelationType.get_by_id(key)
            if ct is not None:
                cls.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set("RelationType::Name::{0}".format(ct.name), ct)
        cache.set("RelationType::ID::{0}".format(ct.id), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete("RelationType::Name::{0}".format(ct.name))
            cache.delete("RelationType::ID::{0}".format(ct.id))


class CITypeAttributeCache(object):
    """
    key is type_id or type_name
    """

    @classmethod
    def get(cls, key):
        if key is None:
            return

        attrs = cache.get("CITypeAttribute::Name::{0}".format(key)) \
            or cache.get("CITypeAttribute::ID::{0}".format(key))
        if not attrs:
            attrs = CITypeAttribute.get_by(type_id=key, to_dict=False)
            if not attrs:
                ci_type = CIType.get_by(name=key, first=True, to_dict=False)
                if ci_type is not None:
                    attrs = CITypeAttribute.get_by(type_id=ci_type.id, to_dict=False)
            if attrs is not None:
                cls.set(key, attrs)
        return attrs

    @classmethod
    def set(cls, key, values):
        ci_type = CITypeCache.get(key)
        if ci_type is not None:
            cache.set("CITypeAttribute::ID::{0}".format(ci_type.id), values)
            cache.set("CITypeAttribute::Name::{0}".format(ci_type.name), values)

    @classmethod
    def clean(cls, key):
        ci_type = CITypeCache.get(key)
        attrs = cls.get(key)
        if attrs is not None and ci_type:
            cache.delete("CITypeAttribute::ID::{0}".format(ci_type.id))
            cache.delete("CITypeAttribute::Name::{0}".format(ci_type.name))
