# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import requests
from flask import current_app

from api.extensions import cache
from api.extensions import db
from api.lib.cmdb.custom_dashboard import CustomDashboardManager
from api.models.cmdb import Attribute
from api.models.cmdb import CI
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


class CITypeAttributesCache(object):
    """
    key is type_id or type_name
    """

    PREFIX_ID = "CITypeAttributes::TypeID::{0}"
    PREFIX_NAME = "CITypeAttributes::TypeName::{0}"

    PREFIX_ID2 = "CITypeAttributes2::TypeID::{0}"
    PREFIX_NAME2 = "CITypeAttributes2::TypeName::{0}"

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
    def get2(cls, key):
        """
        return [(type_attr, attr), ]
        :param key:
        :return:
        """
        if key is None:
            return

        attrs = cache.get(cls.PREFIX_NAME2.format(key))
        attrs = attrs or cache.get(cls.PREFIX_ID2.format(key))
        if not attrs:
            attrs = CITypeAttribute.get_by(type_id=key, to_dict=False)
            if not attrs:
                ci_type = CIType.get_by(name=key, first=True, to_dict=False)
                if ci_type is not None:
                    attrs = CITypeAttribute.get_by(type_id=ci_type.id, to_dict=False)
            if attrs is not None:
                attrs = [(i, AttributeCache.get(i.attr_id)) for i in attrs]
                cls.set2(key, attrs)
        return attrs

    @classmethod
    def set(cls, key, values):
        ci_type = CITypeCache.get(key)
        if ci_type is not None:
            cache.set(cls.PREFIX_ID.format(ci_type.id), values)
            cache.set(cls.PREFIX_NAME.format(ci_type.name), values)

    @classmethod
    def set2(cls, key, values):
        ci_type = CITypeCache.get(key)
        if ci_type is not None:
            cache.set(cls.PREFIX_ID2.format(ci_type.id), values)
            cache.set(cls.PREFIX_NAME2.format(ci_type.name), values)

    @classmethod
    def clean(cls, key):
        ci_type = CITypeCache.get(key)
        attrs = cls.get(key)
        if attrs is not None and ci_type:
            cache.delete(cls.PREFIX_ID.format(ci_type.id))
            cache.delete(cls.PREFIX_NAME.format(ci_type.name))

        attrs2 = cls.get2(key)
        if attrs2 is not None and ci_type:
            cache.delete(cls.PREFIX_ID2.format(ci_type.id))
            cache.delete(cls.PREFIX_NAME2.format(ci_type.name))


class CITypeAttributeCache(object):
    """
    key is type_id  & attr_id
    """

    PREFIX_ID = "CITypeAttribute::TypeID::{0}::AttrID::{1}"

    @classmethod
    def get(cls, type_id, attr_id):

        attr = cache.get(cls.PREFIX_ID.format(type_id, attr_id))
        attr = attr or cache.get(cls.PREFIX_ID.format(type_id, attr_id))
        if not attr:
            attr = CITypeAttribute.get_by(type_id=type_id, attr_id=attr_id, first=True, to_dict=False)
            if attr is not None:
                cls.set(type_id, attr_id, attr)
        return attr

    @classmethod
    def set(cls, type_id, attr_id, attr):
        cache.set(cls.PREFIX_ID.format(type_id, attr_id), attr)

    @classmethod
    def clean(cls, type_id, attr_id):
        cache.delete(cls.PREFIX_ID.format(type_id, attr_id))


class CMDBCounterCache(object):
    KEY = 'CMDB::Counter'

    @classmethod
    def get(cls):
        result = cache.get(cls.KEY) or {}

        if not result:
            result = cls.reset()

        return result

    @classmethod
    def set(cls, result):
        cache.set(cls.KEY, result, timeout=0)

    @classmethod
    def reset(cls):
        customs = CustomDashboardManager.get()
        result = {}
        for custom in customs:
            if custom['category'] == 0:
                result[custom['id']] = cls.summary_counter(custom['type_id'])
            elif custom['category'] == 1:
                result[custom['id']] = cls.attribute_counter(custom['type_id'], custom['attr_id'])
            elif custom['category'] == 2:
                result[custom['id']] = cls.relation_counter(custom['type_id'], custom['level'])

        cls.set(result)

        return result

    @classmethod
    def update(cls, custom):
        result = cache.get(cls.KEY) or {}
        if not result:
            result = cls.reset()

        if custom['category'] == 0:
            result[custom['id']] = cls.summary_counter(custom['type_id'])
        elif custom['category'] == 1:
            result[custom['id']] = cls.attribute_counter(custom['type_id'], custom['attr_id'])
        elif custom['category'] == 2:
            result[custom['id']] = cls.relation_counter(custom['type_id'], custom['level'])

        cls.set(result)

    @staticmethod
    def summary_counter(type_id):
        return db.session.query(CI.id).filter(CI.deleted.is_(False)).filter(CI.type_id == type_id).count()

    @staticmethod
    def relation_counter(type_id, level):

        uri = current_app.config.get('CMDB_API')

        type_names = requests.get("{}/ci/s?q=_type:{}&count=10000".format(uri, type_id)).json().get('result')
        type_id_names = [(str(i.get('_id')), i.get(i.get('unique'))) for i in type_names]

        url = "{}/ci_relations/statistics?root_ids={}&level={}".format(
            uri, ','.join([i[0] for i in type_id_names]), level)
        stats = requests.get(url).json()

        id2name = dict(type_id_names)
        type_ids = set()
        for i in (stats.get('detail') or []):
            for j in stats['detail'][i]:
                type_ids.add(j)

        for type_id in type_ids:
            _type = CITypeCache.get(type_id)
            id2name[type_id] = _type and _type.alias

        result = dict(summary={}, detail={})
        for i in stats:
            if i == "detail":
                for j in stats['detail']:
                    if id2name[j]:
                        result['detail'][id2name[j]] = stats['detail'][j]
                        result['detail'][id2name[j]] = dict()
                        for _j in stats['detail'][j]:
                            result['detail'][id2name[j]][id2name[_j]] = stats['detail'][j][_j]
            elif id2name.get(i):
                result['summary'][id2name[i]] = stats[i]

        return result

    @staticmethod
    def attribute_counter(type_id, attr_id):
        uri = current_app.config.get('CMDB_API')
        url = "{}/ci/s?q=_type:{}&fl={}&facet={}".format(uri, type_id, attr_id, attr_id)
        res = requests.get(url).json()
        if res.get('facet'):
            return dict([i[:2] for i in list(res.get('facet').values())[0]])
