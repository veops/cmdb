# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from api.extensions import cache
from api.models.cmdb import Attribute
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import RelationType


class AttributeCache(object):
    PREFIX_ID = 'Field::ID::{0}'
    PREFIX_NAME = 'Field::Name::{0}'
    PREFIX_ALIAS = 'Field::Alias::{0}'

    @classmethod
    def get(cls, key):
        if key is None:
            return
        attr = cache.get(cls.PREFIX_NAME.format(key))
        attr = attr or cache.get(cls.PREFIX_ID.format(key))
        attr = attr or cache.get(cls.PREFIX_ALIAS.format(key))

        if attr is None:
            attr = Attribute.get_by(name=key, first=True, to_dict=False)
            attr = attr or Attribute.get_by_id(key)
            attr = attr or Attribute.get_by(alias=key, first=True, to_dict=False)
            if attr is not None:
                cls.set(attr)
        return attr

    @classmethod
    def set(cls, attr):
        cache.set(cls.PREFIX_ID.format(attr.id), attr)
        cache.set(cls.PREFIX_NAME.format(attr.name), attr)
        cache.set(cls.PREFIX_ALIAS.format(attr.alias), attr)

    @classmethod
    def clean(cls, attr):
        cache.delete(cls.PREFIX_ID.format(attr.id))
        cache.delete(cls.PREFIX_NAME.format(attr.name))
        cache.delete(cls.PREFIX_ALIAS.format(attr.alias))


class CITypeCache(object):
    PREFIX_ID = "CIType::ID::{0}"
    PREFIX_NAME = "CIType::Name::{0}"
    PREFIX_ALIAS = "CIType::Alias::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get(cls.PREFIX_NAME.format(key))
        ct = ct or cache.get(cls.PREFIX_ID.format(key))
        ct = ct or cache.get(cls.PREFIX_ALIAS.format(key))
        if ct is None:
            ct = CIType.get_by(name=key, first=True, to_dict=False)
            ct = ct or CIType.get_by_id(key)
            ct = ct or CIType.get_by(alias=key, first=True, to_dict=False)
            if ct is not None:
                cls.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set(cls.PREFIX_NAME.format(ct.name), ct)
        cache.set(cls.PREFIX_ID.format(ct.id), ct)
        cache.set(cls.PREFIX_ALIAS.format(ct.alias), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete(cls.PREFIX_NAME.format(ct.name))
            cache.delete(cls.PREFIX_ID.format(ct.id))
            cache.delete(cls.PREFIX_ALIAS.format(ct.alias))


class RelationTypeCache(object):
    PREFIX_ID = "RelationType::ID::{0}"
    PREFIX_NAME = "RelationType::Name::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get(cls.PREFIX_NAME.format(key))
        ct = ct or cache.get(cls.PREFIX_ID.format(key))
        if ct is None:
            ct = RelationType.get_by(name=key, first=True, to_dict=False) or RelationType.get_by_id(key)
            if ct is not None:
                cls.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set(cls.PREFIX_NAME.format(ct.name), ct)
        cache.set(cls.PREFIX_ID.format(ct.id), ct)

    @classmethod
    def clean(cls, key):
        ct = cls.get(key)
        if ct is not None:
            cache.delete(cls.PREFIX_NAME.format(ct.name))
            cache.delete(cls.PREFIX_ID.format(ct.id))


class CITypeAttributeCache(object):
    """
    key is type_id or type_name
    """

    PREFIX_ID = "CITypeAttribute::ID::{0}"
    PREFIX_NAME = "CITypeAttribute::Name::{0}"

    @classmethod
    def get(cls, key):
        if key is None:
            return

        attrs = cache.get(cls.PREFIX_NAME.format(key))
        attrs = attrs or cache.get(cls.PREFIX_ID.format(key))
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
            cache.set(cls.PREFIX_ID.format(ci_type.id), values)
            cache.set(cls.PREFIX_NAME.format(ci_type.name), values)

    @classmethod
    def clean(cls, key):
        ci_type = CITypeCache.get(key)
        attrs = cls.get(key)
        if attrs is not None and ci_type:
            cache.delete(cls.PREFIX_ID.format(ci_type.id))
            cache.delete(cls.PREFIX_NAME.format(ci_type.name))
