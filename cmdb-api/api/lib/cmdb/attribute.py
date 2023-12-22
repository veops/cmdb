# -*- coding:utf-8 -*-

from flask import abort
from flask import current_app
from flask import session
from flask_login import current_user

from api.extensions import db
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import BUILTIN_KEYWORDS
from api.lib.cmdb.const import CITypeOperateType
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import CITypeHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.decorator import kwargs_required
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.lib.webhook import webhook_request
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
    def _get_choice_values_from_webhook(choice_webhook, payload=None):
        ret_key = choice_webhook.get('ret_key')

        try:
            res = webhook_request(choice_webhook, payload or {}).json()
            if ret_key:
                ret_key_list = ret_key.strip().split("##")
                for key in ret_key_list[:-1]:
                    if key in res:
                        res = res[key]
                if isinstance(res, list):
                    return [[i[ret_key_list[-1]], {}] for i in res if i.get(ret_key_list[-1])]

                return [[i, {}] for i in (res.get(ret_key_list[-1]) or [])]

        except Exception as e:
            current_app.logger.error("get choice values failed: {}".format(e))
            return []

    @staticmethod
    def _get_choice_values_from_other(choice_other):
        from api.lib.cmdb.search import SearchError
        from api.lib.cmdb.search.ci import search

        if choice_other.get('type_ids'):
            type_ids = choice_other.get('type_ids')
            attr_id = choice_other.get('attr_id')
            other_filter = choice_other.get('filter') or ''

            query = "_type:({}),{}".format(";".join(map(str, type_ids)), other_filter)
            s = search(query, fl=[str(attr_id)], facet=[str(attr_id)], count=1)
            try:
                _, _, _, _, _, facet = s.search()
                return [[i[0], {}] for i in (list(facet.values()) or [[]])[0]]
            except SearchError as e:
                current_app.logger.error("get choice values from other ci failed: {}".format(e))
                return []

        elif choice_other.get('script'):
            try:
                x = compile(choice_other['script'], '', "exec")
                local_ns = {}
                exec(x, {}, local_ns)
                res = local_ns['ChoiceValue']().values() or []
                return [[i, {}] for i in res]
            except Exception as e:
                current_app.logger.error("get choice values from script: {}".format(e))
                return []

    @classmethod
    def get_choice_values(cls, attr_id, value_type, choice_web_hook, choice_other,
                          choice_web_hook_parse=True, choice_other_parse=True):
        if choice_web_hook:
            if choice_web_hook_parse and isinstance(choice_web_hook, dict):
                return cls._get_choice_values_from_webhook(choice_web_hook)
            else:
                return []
        elif choice_other:
            if choice_other_parse and isinstance(choice_other, dict):
                return cls._get_choice_values_from_other(choice_other)
            else:
                return []

        choice_table = ValueTypeMap.choice.get(value_type)
        if not choice_table:
            return []
        choice_values = choice_table.get_by(fl=["value", "option"], attr_id=attr_id)

        return [[ValueTypeMap.serialize[value_type](choice_value['value']), choice_value['option']]
                for choice_value in choice_values]

    @staticmethod
    def add_choice_values(_id, value_type, choice_values):
        choice_table = ValueTypeMap.choice.get(value_type)
        if choice_table is None:
            return

        choice_table.get_by(attr_id=_id, only_query=True).delete()

        for v, option in choice_values:
            choice_table.create(attr_id=_id, value=v, option=option, commit=False)

        try:
            db.session.flush()
        except Exception as e:
            current_app.logger.warning("add choice values failed: {}".format(e))
            return abort(400, ErrFormat.invalid_choice_values)

    @staticmethod
    def _del_choice_values(_id, value_type):
        choice_table = ValueTypeMap.choice.get(value_type)

        choice_table and choice_table.get_by(attr_id=_id, only_query=True).delete()
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
            attr["is_choice"] and attr.update(
                dict(choice_value=cls.get_choice_values(attr["id"], attr["value_type"],
                                                        attr["choice_web_hook"], attr.get("choice_other"))))
            attr['is_choice'] and attr.pop('choice_web_hook', None)

            res.append(attr)

        return numfound, res

    def get_attribute_by_name(self, name):
        attr = Attribute.get_by(name=name, first=True)
        if attr.get("is_choice"):
            attr["choice_value"] = self.get_choice_values(attr["id"], attr["value_type"],
                                                          attr["choice_web_hook"], attr.get("choice_other"))

        return attr

    def get_attribute_by_alias(self, alias):
        attr = Attribute.get_by(alias=alias, first=True)
        if attr.get("is_choice"):
            attr["choice_value"] = self.get_choice_values(attr["id"], attr["value_type"],
                                                          attr["choice_web_hook"], attr.get("choice_other"))

        return attr

    def get_attribute_by_id(self, _id):
        attr = Attribute.get_by_id(_id).to_dict()
        if attr.get("is_choice"):
            attr["choice_value"] = self.get_choice_values(attr["id"], attr["value_type"],
                                                          attr["choice_web_hook"], attr.get("choice_other"))

        return attr

    def get_attribute(self, key, choice_web_hook_parse=True, choice_other_parse=True):
        attr = AttributeCache.get(key) or dict()
        attr = attr and attr.to_dict()
        if attr.get("is_choice"):
            attr["choice_value"] = self.get_choice_values(
                attr["id"],
                attr["value_type"],
                attr["choice_web_hook"],
                attr.get("choice_other"),
                choice_web_hook_parse=choice_web_hook_parse,
                choice_other_parse=choice_other_parse,
            )

        return attr

    @staticmethod
    def can_create_computed_attribute():
        if RoleEnum.CONFIG not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin('cmdb'):
            return abort(403, ErrFormat.role_required.format(RoleEnum.CONFIG))

    @classmethod
    def calc_computed_attribute(cls, attr_id):
        """
        calculate computed attribute for all ci
        :param attr_id:
        :return:
        """
        cls.can_create_computed_attribute()

        from api.tasks.cmdb import calc_computed_attribute

        calc_computed_attribute.apply_async(args=(attr_id, current_user.uid), queue=CMDB_QUEUE)

    @classmethod
    @kwargs_required("name")
    def add(cls, **kwargs):
        choice_value = kwargs.pop("choice_value", [])
        kwargs.pop("is_choice", None)
        is_choice = True if choice_value or kwargs.get('choice_web_hook') or kwargs.get('choice_other') else False

        name = kwargs.pop("name")
        if name in BUILTIN_KEYWORDS:
            return abort(400, ErrFormat.attribute_name_cannot_be_builtin)

        while kwargs.get('choice_other'):
            if isinstance(kwargs['choice_other'], dict):
                if kwargs['choice_other'].get('script'):
                    break

                if kwargs['choice_other'].get('type_ids') and kwargs['choice_other'].get('attr_id'):
                    break

            return abort(400, ErrFormat.attribute_choice_other_invalid)

        alias = kwargs.pop("alias", "")
        alias = name if not alias else alias
        Attribute.get_by(name=name, first=True) and abort(400, ErrFormat.attribute_name_duplicate.format(name))

        if kwargs.get('default') and not (isinstance(kwargs['default'], dict) and 'default' in kwargs['default']):
            kwargs['default'] = dict(default=kwargs['default'])

        kwargs.get('is_computed') and cls.can_create_computed_attribute()

        kwargs.get('choice_other') and kwargs['choice_other'].get('script') and cls.can_create_computed_attribute()

        attr = Attribute.create(flush=True,
                                name=name,
                                alias=alias,
                                is_choice=is_choice,
                                uid=current_user.uid,
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
    def _clean_ci_type_attributes_cache(attr_id):
        for i in CITypeAttribute.get_by(attr_id=attr_id, to_dict=False):
            CITypeAttributesCache.clean(i.type_id)

    @staticmethod
    def _change_index(attr, old, new):
        from api.lib.cmdb.utils import TableMap
        from api.tasks.cmdb import batch_ci_cache
        from api.lib.cmdb.const import CMDB_QUEUE

        old_table = TableMap(attr=attr, is_index=old).table
        new_table = TableMap(attr=attr, is_index=new).table

        ci_ids = []
        for i in old_table.get_by(attr_id=attr.id, to_dict=False):
            new_table.create(ci_id=i.ci_id, attr_id=attr.id, value=i.value, flush=True)
            ci_ids.append(i.ci_id)

        old_table.get_by(attr_id=attr.id, only_query=True).delete()

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

        if attr.uid == current_user.uid:
            return True

        for i in CITypeAttribute.get_by(attr_id=attr.id, to_dict=False):
            resource = CITypeManager.get_name_by_id(i.type_id)
            if resource:
                validate_permission(resource, ResourceTypeEnum.CI, PermEnum.CONFIG, "cmdb")

        return True

    def update(self, _id, **kwargs):
        attr = Attribute.get_by_id(_id) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_id)))

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

        while kwargs.get('choice_other'):
            if isinstance(kwargs['choice_other'], dict):
                if kwargs['choice_other'].get('script'):
                    break

                if kwargs['choice_other'].get('type_ids') and kwargs['choice_other'].get('attr_id'):
                    break

            return abort(400, ErrFormat.attribute_choice_other_invalid)

        existed2 = attr.to_dict()
        if not existed2['choice_web_hook'] and not existed2.get('choice_other') and existed2['is_choice']:
            existed2['choice_value'] = self.get_choice_values(attr.id, attr.value_type, None, None)

        choice_value = kwargs.pop("choice_value", False)
        is_choice = True if choice_value or kwargs.get('choice_web_hook') or kwargs.get('choice_other') else False
        kwargs['is_choice'] = is_choice

        if kwargs.get('default') and not (isinstance(kwargs['default'], dict) and 'default' in kwargs['default']):
            kwargs['default'] = dict(default=kwargs['default'])

        kwargs.get('is_computed') and self.can_create_computed_attribute()

        is_changed = False
        for k in kwargs:
            if kwargs[k] != getattr(attr, k, None):
                is_changed = True

        if is_changed and not self._can_edit_attribute(attr):
            return abort(403, ErrFormat.cannot_edit_attribute)

        attr.update(flush=True, filter_none=False, **kwargs)

        if is_choice and choice_value:
            self.add_choice_values(attr.id, attr.value_type, choice_value)
        elif existed2['is_choice']:
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

        self._clean_ci_type_attributes_cache(_id)

        return attr.id

    @staticmethod
    def delete(_id):
        attr = Attribute.get_by_id(_id) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_id)))
        name = attr.name

        if CIType.get_by(unique_id=attr.id, first=True, to_dict=False) is not None:
            return abort(400, ErrFormat.attribute_is_unique_id)

        ref = CITypeAttribute.get_by(attr_id=_id, to_dict=False, first=True)
        if ref is not None:
            ci_type = CITypeCache.get(ref.type_id)
            return abort(400, ErrFormat.attribute_is_ref_by_type.format(ci_type and ci_type.alias or ref.type_id))

        if attr.uid != current_user.uid and not is_app_admin('cmdb'):
            return abort(403, ErrFormat.cannot_delete_attribute)

        if attr.is_choice:
            choice_table = ValueTypeMap.choice.get(attr.value_type)
            choice_table.get_by(attr_id=_id, only_query=True).delete()

        attr.soft_delete()

        AttributeCache.clean(attr)

        for i in PreferenceShowAttributes.get_by(attr_id=_id, to_dict=False):
            i.soft_delete(commit=False)

        for i in CITypeAttributeGroupItem.get_by(attr_id=_id, to_dict=False):
            i.soft_delete(commit=False)

        db.session.commit()

        return name
