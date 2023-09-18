# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import current_app

from api.extensions import cache
from api.lib.cmdb.custom_dashboard import CustomDashboardManager
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
        attr = attr or CITypeAttribute.get_by(type_id=type_id, attr_id=attr_id, first=True, to_dict=False)

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
                res = cls.sum_counter(custom)
            elif custom['category'] == 1:
                res = cls.attribute_counter(custom)
            else:
                res = cls.relation_counter(custom.get('type_id'),
                                           custom.get('level'),
                                           custom.get('options', {}).get('filter', ''),
                                           custom.get('options', {}).get('type_ids', ''))

            if res:
                result[custom['id']] = res

        cls.set(result)

        return result

    @classmethod
    def update(cls, custom, flush=True):
        result = cache.get(cls.KEY) or {}
        if not result:
            result = cls.reset()

        if custom['category'] == 0:
            res = cls.sum_counter(custom)
        elif custom['category'] == 1:
            res = cls.attribute_counter(custom)
        else:
            res = cls.relation_counter(custom.get('type_id'),
                                       custom.get('level'),
                                       custom.get('options', {}).get('filter', ''),
                                       custom.get('options', {}).get('type_ids', ''))

        if res and flush:
            result[custom['id']] = res
            cls.set(result)

        return res

    @staticmethod
    def relation_counter(type_id, level, other_filer, type_ids):
        from api.lib.cmdb.search.ci_relation.search import Search as RelSearch
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search

        query = "_type:{}".format(type_id)
        s = search(query, count=1000000)
        try:
            type_names, _, _, _, _, _ = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return

        type_id_names = [(str(i.get('_id')), i.get(i.get('unique'))) for i in type_names]

        s = RelSearch([i[0] for i in type_id_names], level, other_filer or '')
        try:
            stats = s.statistics(type_ids)
        except SearchError as e:
            current_app.logger.error(e)
            return

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
    def attribute_counter(custom):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search
        from api.lib.cmdb.utils import ValueTypeMap

        custom.setdefault('options', {})
        type_id = custom.get('type_id')
        attr_id = custom.get('attr_id')
        type_ids = custom['options'].get('type_ids') or (type_id and [type_id])
        attr_ids = list(map(str, custom['options'].get('attr_ids') or (attr_id and [attr_id])))
        try:
            attr2value_type = [AttributeCache.get(i).value_type for i in attr_ids]
        except AttributeError:
            return

        other_filter = custom['options'].get('filter')
        other_filter = "{}".format(other_filter) if other_filter else ''

        if custom['options'].get('ret') == 'cis':
            query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
            s = search(query, fl=attr_ids, ret_key='alias', count=100)
            try:
                cis, _, _, _, _, _ = s.search()
            except SearchError as e:
                current_app.logger.error(e)
                return

            return cis

        result = dict()
        # level = 1
        query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
        s = search(query, fl=attr_ids, facet=[attr_ids[0]], count=1)
        try:
            _, _, _, _, _, facet = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return
        for i in (list(facet.values()) or [[]])[0]:
            result[ValueTypeMap.serialize2[attr2value_type[0]](str(i[0]))] = i[1]
        if len(attr_ids) == 1:
            return result

        # level = 2
        for v in result:
            query = "_type:({}),{},{}:{}".format(";".join(map(str, type_ids)), other_filter, attr_ids[0], v)
            s = search(query, fl=attr_ids, facet=[attr_ids[1]], count=1)
            try:
                _, _, _, _, _, facet = s.search()
            except SearchError as e:
                current_app.logger.error(e)
                return
            result[v] = dict()
            for i in (list(facet.values()) or [[]])[0]:
                result[v][ValueTypeMap.serialize2[attr2value_type[1]](str(i[0]))] = i[1]

        if len(attr_ids) == 2:
            return result

        # level = 3
        for v1 in result:
            if not isinstance(result[v1], dict):
                continue
            for v2 in result[v1]:
                query = "_type:({}),{},{}:{},{}:{}".format(";".join(map(str, type_ids)), other_filter,
                                                           attr_ids[0], v1, attr_ids[1], v2)
                s = search(query, fl=attr_ids, facet=[attr_ids[2]], count=1)
                try:
                    _, _, _, _, _, facet = s.search()
                except SearchError as e:
                    current_app.logger.error(e)
                    return
                result[v1][v2] = dict()
                for i in (list(facet.values()) or [[]])[0]:
                    result[v1][v2][ValueTypeMap.serialize2[attr2value_type[2]](str(i[0]))] = i[1]

        return result

    @staticmethod
    def sum_counter(custom):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search

        custom.setdefault('options', {})
        type_id = custom.get('type_id')
        type_ids = custom['options'].get('type_ids') or (type_id and [type_id])
        other_filter = custom['options'].get('filter') or ''

        query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
        s = search(query, count=1)
        try:
            _, _, _, _, numfound, _ = s.search()
        except SearchError as e:
            current_app.logger.error(e)
            return

        return numfound
