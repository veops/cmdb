# -*- coding:utf-8 -*- 

import requests
from flask import abort
from flask import current_app
from flask import g
from flask import session

from api.extensions import db
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import CITypeOperateType
from api.lib.cmdb.const import ResourceTypeEnum, RoleEnum, PermEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import CITypeHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.decorator import kwargs_required
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.models.cmdb import Attribute
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeAttributeGroupItem
from api.models.cmdb import PreferenceShowAttributes


class AttributeManager(object):
    """
    CI attributes manager
    """
    cls = Attribute

    def __init__(self):
        pass

    @staticmethod
    def _get_choice_values_from_web_hook(choice_web_hook):
        url = choice_web_hook.get('url')
        ret_key = choice_web_hook.get('ret_key')
        headers = choice_web_hook.get('headers') or {}
        payload = choice_web_hook.get('payload') or {}
        method = choice_web_hook.get('method', 'GET').lower()

        try:
            res = getattr(requests, method)(url, headers=headers, data=payload).json()
            if ret_key:
                ret_key_list = ret_key.strip().split("##")
                for key in ret_key_list[:-1]:
                    if key in res:
                        res = res[key]
                if isinstance(res, list):
                    return [[i[ret_key_list[-1]], {}] for i in res if i.get(ret_key_list[-1])]

                return [[i, {}] for i in (res.get(ret_key_list[-1]) or [])]

        except Exception as e:
            current_app.logger.error(str(e))
            return []

    @classmethod
    def get_choice_values(cls, attr_id, value_type, choice_web_hook, choice_web_hook_parse=True):
        if choice_web_hook and isinstance(choice_web_hook, dict) and choice_web_hook_parse:
            return cls._get_choice_values_from_web_hook(choice_web_hook)
        elif choice_web_hook and not choice_web_hook_parse:
            return []

        choice_table = ValueTypeMap.choice.get(value_type)
        choice_values = choice_table.get_by(fl=["value", "option"], attr_id=attr_id)

        return [[choice_value['value'], choice_value['option']] for choice_value in choice_values]

    @staticmethod
    def add_choice_values(_id, value_type, choice_values):
        choice_table = ValueTypeMap.choice.get(value_type)

        db.session.query(choice_table).filter(choice_table.attr_id == _id).delete()
        db.session.flush()
        choice_values = choice_values
        for v, option in choice_values:
            table = choice_table(attr_id=_id, value=v, option=option)

            db.session.add(table)

        try:
            db.session.flush()
        except:
            return abort(400, ErrFormat.invalid_choice_values)

    @staticmethod
    def _del_choice_values(_id, value_type):
        choice_table = ValueTypeMap.choice.get(value_type)

        db.session.query(choice_table).filter(choice_table.attr_id == _id).delete()
        db.session.flush()

    @classmethod
    def search_attributes(cls, name=None, alias=None, page=1, page_size=None):
        """
        :param name: 
        :param alias: 
        :param page: 
        :param page_size: 
        :return: attribute, if name is None, then return all attributes
        """
        if name is not None:
            attrs = Attribute.get_by_like(name=name)
        elif alias is not None:
            attrs = Attribute.get_by_like(alias=alias)
        else:
            attrs = Attribute.get_by()

        numfound = len(attrs)
        attrs = attrs[(page - 1) * page_size:][:page_size]
        res = list()
        for attr in attrs:
            attr["is_choice"] and attr.update(dict(choice_value=cls.get_choice_values(
                attr["id"], attr["value_type"], attr["choice_web_hook"])))
            attr['is_choice'] and attr.pop('choice_web_hook', None)

            res.append(attr)

        return numfound, res

    def get_attribute_by_name(self, name):
        attr = Attribute.get_by(name=name, first=True)
        if attr and attr["is_choice"]:
            attr.update(dict(choice_value=self.get_choice_values(
                attr["id"], attr["value_type"], attr["choice_web_hook"])))
        return attr

    def get_attribute_by_alias(self, alias):
        attr = Attribute.get_by(alias=alias, first=True)
        if attr and attr["is_choice"]:
            attr.update(dict(choice_value=self.get_choice_values(
                attr["id"], attr["value_type"], attr["choice_web_hook"])))
        return attr

    def get_attribute_by_id(self, _id):
        attr = Attribute.get_by_id(_id).to_dict()
        if attr and attr["is_choice"]:
            attr.update(dict(choice_value=self.get_choice_values(
                attr["id"], attr["value_type"], attr["choice_web_hook"])))
        return attr

    def get_attribute(self, key, choice_web_hook_parse=True):
        attr = AttributeCache.get(key).to_dict()
        if attr and attr["is_choice"]:
            attr.update(dict(choice_value=self.get_choice_values(
                attr["id"], attr["value_type"], attr["choice_web_hook"])), choice_web_hook_parse=choice_web_hook_parse)
        return attr

    @staticmethod
    def can_create_computed_attribute():
        if RoleEnum.CONFIG not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin('cmdb'):
            return abort(403, ErrFormat.role_required.format(RoleEnum.CONFIG))

    @classmethod
    @kwargs_required("name")
    def add(cls, **kwargs):
        choice_value = kwargs.pop("choice_value", [])
        kwargs.pop("is_choice", None)
        is_choice = True if choice_value or kwargs.get('choice_web_hook') else False

        name = kwargs.pop("name")
        if name in {'id', '_id', 'ci_id', 'type', '_type', 'ci_type'}:
            return abort(400, ErrFormat.attribute_name_cannot_be_builtin)
        alias = kwargs.pop("alias", "")
        alias = name if not alias else alias
        Attribute.get_by(name=name, first=True) and abort(400, ErrFormat.attribute_name_duplicate.format(name))

        if kwargs.get('default') and not (isinstance(kwargs['default'], dict) and 'default' in kwargs['default']):
            kwargs['default'] = dict(default=kwargs['default'])

        kwargs.get('is_computed') and cls.can_create_computed_attribute()

        attr = Attribute.create(flush=True,
                                name=name,
                                alias=alias,
                                is_choice=is_choice,
                                uid=g.user.uid,
                                **kwargs)

        if choice_value:
            cls.add_choice_values(attr.id, attr.value_type, choice_value)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("add attribute error, {0}".format(str(e)))

            return abort(400, ErrFormat.add_attribute_failed.format(name))

        AttributeCache.clean(attr)

        if current_app.config.get("USE_ES"):
            from api.extensions import es
            other = dict()
            other['index'] = True if attr.is_index else False
            if attr.value_type == ValueTypeEnum.TEXT:
                other['analyzer'] = 'ik_max_word'
                other['search_analyzer'] = 'ik_smart'
                if attr.is_index:
                    other["fields"] = {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
            es.update_mapping(name, ValueTypeMap.es_type[attr.value_type], other)

        return attr.id

    @staticmethod
    def _change_index(attr, old, new):
        from api.lib.cmdb.utils import TableMap
        from api.tasks.cmdb import batch_ci_cache
        from api.lib.cmdb.const import CMDB_QUEUE

        old_table = TableMap(attr=attr, is_index=old).table
        new_table = TableMap(attr=attr, is_index=new).table

        ci_ids = []
        for i in db.session.query(old_table).filter(getattr(old_table, 'attr_id') == attr.id):
            new_table.create(ci_id=i.ci_id, attr_id=attr.id, value=i.value, flush=True)
            ci_ids.append(i.ci_id)

        db.session.query(old_table).filter(getattr(old_table, 'attr_id') == attr.id).delete()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            return abort(400, ErrFormat.attribute_index_change_failed)

        batch_ci_cache.apply_async(args=(ci_ids,), queue=CMDB_QUEUE)

    @staticmethod
    def _can_edit_attribute(attr):
        from api.lib.cmdb.ci_type import CITypeManager

        if attr.uid == g.user.uid:
            return True

        for i in CITypeAttribute.get_by(attr_id=attr.id, to_dict=False):
            resource = CITypeManager.get_name_by_id(i.type_id)
            if resource:
                validate_permission(resource, ResourceTypeEnum.CI, PermEnum.CONFIG, "cmdb")

        return True

    def update(self, _id, **kwargs):
        attr = Attribute.get_by_id(_id) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_id)))

        if not self._can_edit_attribute(attr):
            return abort(403, ErrFormat.cannot_edit_attribute)

        if kwargs.get("name"):
            other = Attribute.get_by(name=kwargs['name'], first=True, to_dict=False)
            if other and other.id != attr.id:
                return abort(400, ErrFormat.attribute_name_duplicate.format(kwargs['name']))

        if attr.value_type != kwargs.get('value_type'):
            return abort(400, ErrFormat.attribute_value_type_cannot_change)

        if "is_list" in kwargs and kwargs['is_list'] != attr.is_list:
            return abort(400, ErrFormat.attribute_list_value_cannot_change)

        if "is_index" in kwargs and kwargs['is_index'] != attr.is_index:
            if not is_app_admin("cmdb"):
                return abort(400, ErrFormat.attribute_index_cannot_change)

            self._change_index(attr, attr.is_index, kwargs['is_index'])

        existed2 = attr.to_dict()
        if not existed2['choice_web_hook'] and existed2['is_choice']:
            existed2['choice_value'] = self.get_choice_values(attr.id, attr.value_type, attr.choice_web_hook)

        choice_value = kwargs.pop("choice_value", False)
        is_choice = True if choice_value or kwargs.get('choice_web_hook') else False
        kwargs['is_choice'] = is_choice

        if kwargs.get('default') and not (isinstance(kwargs['default'], dict) and 'default' in kwargs['default']):
            kwargs['default'] = dict(default=kwargs['default'])

        kwargs.get('is_computed') and self.can_create_computed_attribute()

        attr.update(flush=True, filter_none=False, **kwargs)

        if is_choice and choice_value:
            self.add_choice_values(attr.id, attr.value_type, choice_value)
        elif is_choice:
            self._del_choice_values(attr.id, attr.value_type)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("update attribute error, {0}".format(str(e)))

            return abort(400, ErrFormat.update_attribute_failed.format(("id=".format(_id))))

        new = attr.to_dict()
        if not new['choice_web_hook'] and new['is_choice']:
            new['choice_value'] = choice_value
        CITypeHistoryManager.add(CITypeOperateType.UPDATE_ATTRIBUTE, None, attr_id=attr.id,
                                 change=dict(old=existed2, new=new))

        AttributeCache.clean(attr)

        return attr.id

    @staticmethod
    def delete(_id):
        attr = Attribute.get_by_id(_id) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_id)))
        name = attr.name

        if CIType.get_by(unique_id=attr.id, first=True, to_dict=False) is not None:
            return abort(400, ErrFormat.attribute_is_unique_id)

        if attr.uid and attr.uid != g.user.uid:
            return abort(403, ErrFormat.cannot_delete_attribute)

        if attr.is_choice:
            choice_table = ValueTypeMap.choice.get(attr.value_type)
            db.session.query(choice_table).filter(choice_table.attr_id == _id).delete()  # FIXME: session conflict
            db.session.flush()

        AttributeCache.clean(attr)

        attr.soft_delete()

        for i in CITypeAttribute.get_by(attr_id=_id, to_dict=False):
            i.soft_delete()

        for i in PreferenceShowAttributes.get_by(attr_id=_id, to_dict=False):
            i.soft_delete()

        for i in CITypeAttributeGroupItem.get_by(attr_id=_id, to_dict=False):
            i.soft_delete()

        return name
