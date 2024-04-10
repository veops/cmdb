# -*- coding:utf-8 -*-

import copy

import toposort
from flask import abort
from flask import current_app
from flask import session
from flask_login import current_user
from toposort import toposort_flatten
from werkzeug.exceptions import BadRequest

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import CITypeOperateType
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import CITypeHistoryManager
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.relation_type import RelationTypeManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.models.cmdb import Attribute
from api.models.cmdb import AutoDiscoveryCI
from api.models.cmdb import AutoDiscoveryCIType
from api.models.cmdb import CI
from api.models.cmdb import CIFilterPerms
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeAttributeGroup
from api.models.cmdb import CITypeAttributeGroupItem
from api.models.cmdb import CITypeGroup
from api.models.cmdb import CITypeGroupItem
from api.models.cmdb import CITypeInheritance
from api.models.cmdb import CITypeRelation
from api.models.cmdb import CITypeTrigger
from api.models.cmdb import CITypeUniqueConstraint
from api.models.cmdb import CustomDashboard
from api.models.cmdb import PreferenceCITypeOrder
from api.models.cmdb import PreferenceRelationView
from api.models.cmdb import PreferenceSearchOption
from api.models.cmdb import PreferenceShowAttributes
from api.models.cmdb import PreferenceTreeView
from api.models.cmdb import RelationType


class CITypeManager(object):
    """
    manage CIType
    """
    cls = CIType

    def __init__(self):
        pass

    @staticmethod
    def get_name_by_id(type_id):
        ci_type = CITypeCache.get(type_id)

        return ci_type and ci_type.name

    @staticmethod
    def check_is_existed(key):
        ci_type = CITypeCache.get(key) or abort(404, ErrFormat.ci_type_not_found2.format(key))

        return CIType.get_by_id(ci_type.id)

    def get_icons(self):
        return {i.id: i.icon or i.name for i in db.session.query(
            self.cls.id, self.cls.icon, self.cls.name).filter(self.cls.deleted.is_(False))}

    @staticmethod
    def get_ci_types(type_name=None, like=True):
        resources = None
        if current_app.config.get('USE_ACL') and not is_app_admin('cmdb'):
            resources = set([i.get('name') for i in ACLManager().get_resources(ResourceTypeEnum.CI_TYPE)])

        ci_types = CIType.get_by() if type_name is None else (
            CIType.get_by_like(name=type_name) if like else CIType.get_by(name=type_name))
        res = list()
        for type_dict in ci_types:
            attr = AttributeCache.get(type_dict["unique_id"])
            type_dict["unique_key"] = attr and attr.name
            type_dict['parent_ids'] = CITypeInheritanceManager.get_parents(type_dict['id'])
            if resources is None or type_dict['name'] in resources:
                res.append(type_dict)

        return res

    @staticmethod
    def query(_type):
        ci_type = CITypeCache.get(_type) or abort(404, ErrFormat.ci_type_not_found2.format(_type))

        return ci_type.to_dict()

    @staticmethod
    def _validate_unique(type_id=None, name=None, alias=None):
        if name is not None:
            ci_type = CIType.get_by(name=name, first=True, to_dict=False)
        elif alias is not None:
            ci_type = CIType.get_by(alias=alias, first=True, to_dict=False)
        else:
            return

        if not ci_type:
            return

        if type_id is not None and ci_type.id != type_id:
            return abort(400, ErrFormat.ci_type_is_already_existed.format(name or alias))

        if type_id is None and ci_type is not None:
            return abort(400, ErrFormat.ci_type_is_already_existed.format(name or alias))

    @classmethod
    @kwargs_required("name")
    def add(cls, **kwargs):
        if current_app.config.get('USE_ACL') and not is_app_admin('cmdb'):
            if ErrFormat.ci_type_config not in {i['name'] for i in ACLManager().get_resources(ResourceTypeEnum.PAGE)}:
                return abort(403, ErrFormat.no_permission2)

        unique_key = kwargs.pop("unique_key", None) or kwargs.pop("unique_id", None)
        unique_key = AttributeCache.get(unique_key) or abort(404, ErrFormat.unique_key_not_define)

        kwargs["alias"] = kwargs["name"] if not kwargs.get("alias") else kwargs["alias"]

        cls._validate_unique(name=kwargs['name'])
        cls._validate_unique(alias=kwargs['alias'])

        kwargs["unique_id"] = unique_key.id
        kwargs['uid'] = current_user.uid

        parent_ids = kwargs.pop('parent_ids', None)

        ci_type = CIType.create(**kwargs)

        CITypeInheritanceManager.add(parent_ids, ci_type.id)

        CITypeAttributeManager.add(ci_type.id, [unique_key.id], is_required=True)

        CITypeCache.clean(ci_type.name)

        if current_app.config.get("USE_ACL"):
            try:
                ACLManager().add_resource(ci_type.name, ResourceTypeEnum.CI)
            except BadRequest:
                pass

            ACLManager().grant_resource_to_role(ci_type.name,
                                                RoleEnum.CMDB_READ_ALL,
                                                ResourceTypeEnum.CI,
                                                permissions=[PermEnum.READ])
            ACLManager().grant_resource_to_role(ci_type.name,
                                                current_user.username,
                                                ResourceTypeEnum.CI)

        CITypeHistoryManager.add(CITypeOperateType.ADD, ci_type.id, change=ci_type.to_dict())

        return ci_type.id

    @classmethod
    def update(cls, type_id, **kwargs):

        ci_type = cls.check_is_existed(type_id)

        cls._validate_unique(type_id=type_id, name=kwargs.get('name'))
        cls._validate_unique(type_id=type_id, alias=kwargs.get('alias') or kwargs.get('name'))

        unique_key = kwargs.pop("unique_key", None)
        unique_key = AttributeCache.get(unique_key)
        if unique_key is not None:
            kwargs["unique_id"] = unique_key.id
            type_attr = CITypeAttribute.get_by(type_id=type_id,
                                               attr_id=unique_key.id,
                                               first=True,
                                               to_dict=False)
            if type_attr is None:
                CITypeAttributeManager.add(type_id, [unique_key.id], is_required=True)
            elif not type_attr.is_required:
                attr = type_attr.to_dict()
                attr.update(dict(is_required=True))
                CITypeAttributeManager.update(type_id, [attr])

        ci_type2 = ci_type.to_dict()
        new = ci_type.update(**kwargs)

        CITypeCache.clean(type_id)

        if kwargs.get('name') and kwargs['name'] != ci_type2['name'] and current_app.config.get("USE_ACL"):
            ACLManager().update_resource(ci_type2['name'], kwargs['name'], ResourceTypeEnum.CI)

        CITypeHistoryManager.add(CITypeOperateType.UPDATE, ci_type.id,
                                 change=dict(old=ci_type2, new=new.to_dict()))

        return type_id

    @classmethod
    def set_enabled(cls, type_id, enabled=True):
        ci_type = cls.check_is_existed(type_id)
        ci_type.update(enabled=enabled)

        return type_id

    @classmethod
    def delete(cls, type_id):
        ci_type = cls.check_is_existed(type_id)

        if ci_type.uid and ci_type.uid != current_user.uid:
            return abort(403, ErrFormat.only_owner_can_delete)

        if CI.get_by(type_id=type_id, first=True, to_dict=False) is not None:
            return abort(400, ErrFormat.ci_exists_and_cannot_delete_type)

        relation_views = PreferenceRelationView.get_by(to_dict=False)
        for rv in relation_views:
            for item in (rv.cr_ids or []):
                if item.get('parent_id') == type_id or item.get('child_id') == type_id:
                    return abort(400, ErrFormat.ci_relation_view_exists_and_cannot_delete_type.format(rv.name))

        for item in (CITypeRelation.get_by(parent_id=type_id, to_dict=False) +
                     CITypeRelation.get_by(child_id=type_id, to_dict=False)):
            if current_app.config.get('USE_ACL'):
                resource_name = CITypeRelationManager.acl_resource_name(item.parent.name, item.child.name)
                ACLManager().del_resource(resource_name, ResourceTypeEnum.CI_TYPE_RELATION)

            item.soft_delete(commit=False)

        for table in [PreferenceTreeView, PreferenceShowAttributes, PreferenceSearchOption, CustomDashboard,
                      CITypeGroupItem, CITypeAttributeGroup, CITypeAttribute, CITypeUniqueConstraint, CITypeTrigger,
                      AutoDiscoveryCIType, CIFilterPerms, PreferenceCITypeOrder]:
            for item in table.get_by(type_id=type_id, to_dict=False):
                item.soft_delete(commit=False)

        for item in AutoDiscoveryCI.get_by(type_id=type_id, to_dict=False):
            item.delete(commit=False)

        for item in CITypeInheritance.get_by(parent_id=type_id, to_dict=False):
            item.delete(commit=False)

        for item in CITypeInheritance.get_by(child_id=type_id, to_dict=False):
            item.delete(commit=False)

        db.session.commit()

        ci_type.soft_delete()

        CITypeCache.clean(type_id)

        CITypeHistoryManager.add(CITypeOperateType.DELETE, ci_type.id, change=ci_type.to_dict())

        if current_app.config.get("USE_ACL"):
            ACLManager().del_resource(ci_type.name, ResourceTypeEnum.CI)


class CITypeInheritanceManager(object):
    cls = CITypeInheritance

    @classmethod
    def get_parents(cls, type_id):
        return [i.parent_id for i in cls.cls.get_by(child_id=type_id, to_dict=False)]

    @classmethod
    def recursive_children(cls, type_id):
        result = []

        def _get_child(_id):
            children = [i.child_id for i in cls.cls.get_by(parent_id=_id, to_dict=False)]
            result.extend(children)
            for child_id in children:
                _get_child(child_id)

        _get_child(type_id)

        return result

    @classmethod
    def base(cls, type_id):
        result = []
        q = []

        def _get_parents(_type_id):
            parents = [i.parent_id for i in cls.cls.get_by(child_id=_type_id, to_dict=False)]
            for i in parents[::-1]:
                q.append(i)
            try:
                out = q.pop(0)
            except IndexError:
                return

            result.append(out)

            _get_parents(out)

        _get_parents(type_id)

        return result[::-1]

    @classmethod
    def add(cls, parent_ids, child_id):

        rels = {}
        for i in cls.cls.get_by(to_dict=False):
            rels.setdefault(i.child_id, set()).add(i.parent_id)

        try:
            toposort_flatten(rels)
        except toposort.CircularDependencyError as e:
            current_app.logger.warning(str(e))
            return abort(400, ErrFormat.circular_dependency_error)

        for parent_id in parent_ids or []:
            if parent_id == child_id:
                return abort(400, ErrFormat.circular_dependency_error)

            existed = cls.cls.get_by(parent_id=parent_id, child_id=child_id, first=True, to_dict=False)
            if existed is None:
                rels.setdefault(child_id, set()).add(parent_id)
                try:
                    toposort_flatten(rels)
                except toposort.CircularDependencyError as e:
                    current_app.logger.warning(str(e))
                    return abort(400, ErrFormat.circular_dependency_error)

                cls.cls.create(parent_id=parent_id, child_id=child_id, commit=False)

        db.session.commit()

    @classmethod
    def delete(cls, parent_id, child_id):

        existed = cls.cls.get_by(parent_id=parent_id, child_id=child_id, first=True, to_dict=False)

        if existed is not None:
            children = cls.recursive_children(child_id) + [child_id]
            for _id in children:
                if CI.get_by(type_id=_id, to_dict=False, first=True) is not None:
                    return abort(400, ErrFormat.ci_exists_and_cannot_delete_inheritance)

            attr_ids = set([i.id for _, i in CITypeAttributeManager.get_all_attributes(parent_id)])
            for _id in children:
                for attr_id in attr_ids:
                    for i in PreferenceShowAttributes.get_by(type_id=_id, attr_id=attr_id, to_dict=False):
                        i.soft_delete(commit=False)
            db.session.commit()

            existed.soft_delete()


class CITypeGroupManager(object):
    cls = CITypeGroup

    @staticmethod
    def get(need_other=None, config_required=True):
        resources = None
        if current_app.config.get('USE_ACL'):
            resources = ACLManager('cmdb').get_resources(ResourceTypeEnum.CI)
            if config_required:
                resources = {i['name']: i['permissions'] for i in resources if PermEnum.CONFIG in i.get("permissions")}
            else:
                resources = {i['name']: i['permissions'] for i in resources if PermEnum.READ in i.get("permissions")}

        groups = sorted(CITypeGroup.get_by(), key=lambda x: x['order'] or 0)
        group_types = set()
        for group in groups:
            for t in sorted(CITypeGroupItem.get_by(group_id=group['id']), key=lambda x: x['order'] or 0):
                ci_type = CITypeCache.get(t['type_id']).to_dict()
                if resources is None or (ci_type and ci_type['name'] in resources):
                    ci_type['permissions'] = resources[ci_type['name']] if resources is not None else None
                    ci_type['inherited'] = True if CITypeInheritanceManager.get_parents(ci_type['id']) else False
                    group.setdefault("ci_types", []).append(ci_type)
                    group_types.add(t["type_id"])

        if need_other:
            ci_types = CITypeManager.get_ci_types()
            other_types = dict(ci_types=[])
            for ci_type in ci_types:
                if ci_type["id"] not in group_types and (resources is None or ci_type['name'] in resources):
                    ci_type['permissions'] = resources.get(ci_type['name']) if resources is not None else None
                    ci_type['inherited'] = True if CITypeInheritanceManager.get_parents(ci_type['id']) else False
                    other_types['ci_types'].append(ci_type)

            groups.append(other_types)

        return groups

    @staticmethod
    def add(name):
        CITypeGroup.get_by(name=name, first=True) and abort(400, ErrFormat.ci_type_group_exists.format(name))

        return CITypeGroup.create(name=name)

    @staticmethod
    def update(gid, name, type_ids):
        """
        update part
        :param gid:
        :param name:
        :param type_ids:
        :return:
        """
        existed = CITypeGroup.get_by_id(gid) or abort(
            404, ErrFormat.ci_type_group_not_found.format("id={}".format(gid)))
        if name is not None and name != existed.name:
            if RoleEnum.CONFIG not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin("cmdb"):
                return abort(403, ErrFormat.role_required.format(RoleEnum.CONFIG))

            existed.update(name=name)

        max_order = max([i.order or 0 for i in CITypeGroupItem.get_by(group_id=gid, to_dict=False)] or [0])

        i = 1
        existed_items = []
        for type_id in type_ids:

            for other in CITypeGroupItem.get_by(type_id=type_id, to_dict=False):
                if other.group_id != gid:
                    other.soft_delete()

            item = CITypeGroupItem.get_by(group_id=gid, type_id=type_id, first=True, to_dict=False)
            if item is None:
                CITypeGroupItem.create(group_id=gid, type_id=type_id, order=i + max_order)
                i += 1
            else:
                existed_items.append(item)

        orders = sorted([i.order for i in existed_items])
        for i in range(len(existed_items)):
            existed_items[i].update(order=orders[i])

    @staticmethod
    def order(group_ids):
        for idx, group_id in enumerate(group_ids):
            group = CITypeGroup.get_by_id(group_id)
            group and group.update(order=idx)

    @staticmethod
    def delete(gid, type_ids=None):
        type_ids = type_ids or []
        existed = CITypeGroup.get_by_id(gid) or abort(
            404, ErrFormat.ci_type_group_not_found.format("id={}".format(gid)))

        items = CITypeGroupItem.get_by(group_id=gid, to_dict=False)
        for item in items:
            if (type_ids and item.type_id in type_ids) or not type_ids:
                item.soft_delete()

        if not type_ids:
            existed.soft_delete()


class CITypeAttributeManager(object):
    """
    manage CIType's attributes, include query, add, update, delete
    """

    def __init__(self):
        pass

    @staticmethod
    def get_attr_name(ci_type_name, key):
        ci_type = CITypeCache.get(ci_type_name)
        if ci_type is None:
            return

        for i in CITypeAttributesCache.get(ci_type.id):
            attr = AttributeCache.get(i.attr_id)
            if attr and (attr.name == key or attr.alias == key):
                return attr.name

    @staticmethod
    def get_all_attributes(type_id):
        parent_ids = CITypeInheritanceManager.base(type_id)

        result = []
        for _type_id in parent_ids + [type_id]:
            result.extend(CITypeAttributesCache.get2(_type_id))

        return result

    @classmethod
    def get_attr_names_by_type_id(cls, type_id):
        return [attr.name for _, attr in cls.get_all_attributes(type_id)]

    @staticmethod
    def get_attributes_by_type_id(type_id, choice_web_hook_parse=True, choice_other_parse=True):
        has_config_perm = ACLManager('cmdb').has_permission(
            CITypeManager.get_name_by_id(type_id), ResourceTypeEnum.CI, PermEnum.CONFIG)

        parent_ids = CITypeInheritanceManager.base(type_id)

        result = list()
        id2pos = dict()
        type2name = {i: CITypeCache.get(i) for i in parent_ids}
        for _type_id in parent_ids + [type_id]:
            attrs = CITypeAttributesCache.get(_type_id)
            for attr in sorted(attrs, key=lambda x: (x.order, x.id)):
                attr_dict = AttributeManager().get_attribute(attr.attr_id, choice_web_hook_parse, choice_other_parse)
                attr_dict["is_required"] = attr.is_required
                attr_dict["order"] = attr.order
                attr_dict["default_show"] = attr.default_show
                attr_dict["inherited"] = False if _type_id == type_id else True
                attr_dict["inherited_from"] = type2name.get(_type_id) and type2name[_type_id].alias
                if not has_config_perm:
                    attr_dict.pop('choice_web_hook', None)
                    attr_dict.pop('choice_other', None)

                if attr_dict['id'] not in id2pos:
                    id2pos[attr_dict['id']] = len(result)
                    result.append(attr_dict)
                else:
                    result[id2pos[attr_dict['id']]] = attr_dict

        return result

    @classmethod
    def get_common_attributes(cls, type_ids):
        has_config_perm = False
        for type_id in type_ids:
            has_config_perm |= ACLManager('cmdb').has_permission(
                CITypeManager.get_name_by_id(type_id), ResourceTypeEnum.CI, PermEnum.CONFIG)

        result = {type_id: [i for _, i in cls.get_all_attributes(type_id)] for type_id in type_ids}
        attr2types = {}
        for type_id in result:
            for i in result[type_id]:
                attr2types.setdefault(i.id, []).append(type_id)

        attrs = []
        for attr_id in attr2types:
            if len(attr2types[attr_id]) == len(type_ids):
                attr = AttributeManager().get_attribute_by_id(attr_id)
                if not has_config_perm:
                    attr.pop('choice_web_hook', None)
                attrs.append(attr)

        return attrs

    @staticmethod
    def _check(type_id, attr_ids):
        ci_type = CITypeManager.check_is_existed(type_id)

        if not attr_ids or not isinstance(attr_ids, list):
            return abort(400, ErrFormat.argument_value_required.format("attr_ids"))

        for attr_id in attr_ids:
            AttributeCache.get(attr_id) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(attr_id)))

        return ci_type

    @classmethod
    def add(cls, type_id, attr_ids=None, **kwargs):
        """
        add attributes to CIType
        :param type_id:
        :param attr_ids: list
        :param kwargs:
        :return:
        """
        attr_ids = list(set(attr_ids))

        cls._check(type_id, attr_ids)

        for attr_id in attr_ids:
            existed = CITypeAttribute.get_by(type_id=type_id,
                                             attr_id=attr_id,
                                             first=True,
                                             to_dict=False)
            if existed is not None:
                continue

            current_app.logger.debug(attr_id)
            CITypeAttribute.create(type_id=type_id, attr_id=attr_id, **kwargs)

            attr = AttributeCache.get(attr_id)
            CITypeHistoryManager.add(CITypeOperateType.ADD_ATTRIBUTE, type_id, attr_id=attr_id,
                                     change=attr and attr.to_dict())

        CITypeAttributesCache.clean(type_id)

    @classmethod
    def update(cls, type_id, attributes):
        """
        update attributes to CIType
        :param type_id:
        :param attributes: list
        :return:
        """
        cls._check(type_id, [i.get('attr_id') for i in attributes])

        for attr in attributes:
            existed = CITypeAttribute.get_by(type_id=type_id,
                                             attr_id=attr.get("attr_id"),
                                             first=True,
                                             to_dict=False)
            if existed is None:
                continue

            existed2 = existed.to_dict()
            new = existed.update(**attr)

            CITypeAttributeCache.clean(type_id, existed.attr_id)

            attr = AttributeCache.get(attr.get('attr_id'))
            if attr:
                CITypeHistoryManager.add(CITypeOperateType.UPDATE_ATTRIBUTE, type_id, attr_id=attr.id,
                                         change=dict(old=existed2, new=new.to_dict()))

        CITypeAttributesCache.clean(type_id)

    @classmethod
    def delete(cls, type_id, attr_ids=None):
        """
        delete attributes from CIType
        :param type_id:
        :param attr_ids: list
        :return:
        """
        from api.tasks.cmdb import ci_cache

        ci_type = cls._check(type_id, attr_ids)

        for attr_id in attr_ids:
            attr = AttributeCache.get(attr_id)

            if ci_type.default_order_attr == attr.name or ci_type.default_order_attr == "-{}".format(attr.name):
                return abort(400, ErrFormat.cannot_delete_default_order_attr)

            if attr_id == ci_type.unique_id:
                return abort(400, ErrFormat.cannot_delete_unique)

            existed = CITypeAttribute.get_by(type_id=type_id,
                                             attr_id=attr_id,
                                             first=True,
                                             to_dict=False)
            groups = CITypeAttributeGroup.get_by(type_id=type_id, to_dict=False)
            for group in groups:
                CITypeAttributeGroupManager().delete_item(group_id=group.id, attr_id=attr_id)

            if existed is not None:
                existed.soft_delete()

                for ci in CI.get_by(type_id=type_id, to_dict=False):
                    AttributeValueManager.delete_attr_value(attr_id, ci.id, commit=False)

                    ci_cache.apply_async(args=(ci.id, None, None), queue=CMDB_QUEUE)

                for item in PreferenceShowAttributes.get_by(type_id=type_id, attr_id=attr_id, to_dict=False):
                    item.soft_delete(commit=False)

                child_ids = CITypeInheritanceManager.recursive_children(type_id)
                for _type_id in [type_id] + child_ids:
                    for item in CITypeUniqueConstraint.get_by(type_id=_type_id, to_dict=False):
                        if attr_id in item.attr_ids:
                            attr_ids = copy.deepcopy(item.attr_ids)
                            attr_ids.remove(attr_id)

                            if attr_ids:
                                item.update(attr_ids=attr_ids, commit=False)
                            else:
                                item.soft_delete(commit=False)

                    item = CITypeTrigger.get_by(type_id=_type_id, attr_id=attr_id, to_dict=False, first=True)
                    item and item.soft_delete(commit=False)

                for item in (CITypeRelation.get_by(parent_id=type_id, parent_attr_id=attr_id, to_dict=False) +
                             CITypeRelation.get_by(child_id=type_id, child_attr_id=attr_id, to_dict=False)):
                    item.soft_delete(commit=False)

                db.session.commit()

                CITypeAttributeCache.clean(type_id, attr_id)

            CITypeHistoryManager.add(CITypeOperateType.DELETE_ATTRIBUTE, type_id, attr_id=attr.id,
                                     change=attr and attr.to_dict())

        CITypeAttributesCache.clean(type_id)

    @classmethod
    def transfer(cls, type_id, _from, _to):
        current_app.logger.info("[{0}] {1} -> {2}".format(type_id, _from, _to))
        attr_id = _from.get('attr_id')
        from_group_id = _from.get('group_id')
        to_group_id = _to.get('group_id')
        from_group_name = _from.get('group_name')
        to_group_name = _to.get('group_name')
        order = _to.get('order')

        if from_group_name:
            from_group = CITypeAttributeGroup.get_by(type_id=type_id, name=from_group_name, first=True, to_dict=False)
            from_group_id = from_group and from_group.id

        if to_group_name:
            to_group = CITypeAttributeGroup.get_by(type_id=type_id, name=to_group_name, first=True, to_dict=False)
            to_group_id = to_group and to_group.id

            if not to_group_id and CITypeInheritance.get_by(child_id=type_id, to_dict=False):
                to_group = CITypeAttributeGroup.create(type_id=type_id, name=to_group_name)
                to_group_id = to_group and to_group.id

        if from_group_id != to_group_id:
            if from_group_id is not None:
                CITypeAttributeGroupManager.delete_item(from_group_id, attr_id)

            if to_group_id is not None:
                CITypeAttributeGroupManager.add_item(to_group_id, attr_id, order)

        elif from_group_id:
            CITypeAttributeGroupManager.update_item(from_group_id, attr_id, order)

        else:  # other attribute transfer
            return abort(400, ErrFormat.invalid_operation)

        CITypeAttributesCache.clean(type_id)

        from api.tasks.cmdb import ci_type_attribute_order_rebuild
        ci_type_attribute_order_rebuild.apply_async(args=(type_id, current_user.uid), queue=CMDB_QUEUE)


class CITypeRelationManager(object):
    """
    manage relation between CITypes
    """

    @staticmethod
    def get():
        res = CITypeRelation.get_by(to_dict=False)
        type2attributes = dict()
        for idx, item in enumerate(res):
            _item = item.to_dict()
            res[idx] = _item
            res[idx]['parent'] = item.parent.to_dict()
            if item.parent_id not in type2attributes:
                type2attributes[item.parent_id] = [i[1].to_dict() for i in CITypeAttributesCache.get2(item.parent_id)]
            res[idx]['child'] = item.child.to_dict()
            if item.child_id not in type2attributes:
                type2attributes[item.child_id] = [i[1].to_dict() for i in CITypeAttributesCache.get2(item.child_id)]
            res[idx]['relation_type'] = item.relation_type.to_dict()

        return res, type2attributes

    @staticmethod
    def get_child_type_ids(type_id, level):
        ids = [type_id]
        query = db.session.query(CITypeRelation).filter(CITypeRelation.deleted.is_(False))
        for _ in range(0, level):
            ids = [i.child_id for i in query.filter(CITypeRelation.parent_id.in_(ids))]

        return ids

    @staticmethod
    def get_parent_type_ids(type_id, level):
        ids = [type_id]
        query = db.session.query(CITypeRelation).filter(CITypeRelation.deleted.is_(False))
        for _ in range(0, level):
            ids = [i.parent_id for i in query.filter(CITypeRelation.child_id.in_(ids))]

        return ids

    @staticmethod
    def _wrap_relation_type_dict(type_id, relation_inst):
        ci_type_dict = CITypeCache.get(type_id).to_dict()
        ci_type_dict["ctr_id"] = relation_inst.id
        ci_type_dict["attributes"] = CITypeAttributeManager.get_attributes_by_type_id(ci_type_dict["id"])
        attr_filter = CIFilterPermsCRUD.get_attr_filter(type_id)
        if attr_filter:
            ci_type_dict["attributes"] = [attr for attr in (ci_type_dict["attributes"] or [])
                                          if attr['name'] in attr_filter]

        ci_type_dict["relation_type"] = relation_inst.relation_type.name
        ci_type_dict["constraint"] = relation_inst.constraint
        ci_type_dict["parent_attr_id"] = relation_inst.parent_attr_id
        ci_type_dict["child_attr_id"] = relation_inst.child_attr_id

        return ci_type_dict

    @classmethod
    def get_children(cls, parent_id):
        children = CITypeRelation.get_by(parent_id=parent_id, to_dict=False)

        return [cls._wrap_relation_type_dict(child.child_id, child) for child in children]

    @classmethod
    def recursive_level2children(cls, parent_id):
        result = dict()

        def get_children(_id, level):
            children = CITypeRelation.get_by(parent_id=_id, to_dict=False)
            if children:
                result.setdefault(level + 1, []).extend([i.child.to_dict() for i in children])

            for i in children:
                if i.child_id != _id:
                    get_children(i.child_id, level + 1)

        get_children(parent_id, 0)

        return result

    @classmethod
    def get_parents(cls, child_id):
        parents = CITypeRelation.get_by(child_id=child_id, to_dict=False)

        return [cls._wrap_relation_type_dict(parent.parent_id, parent) for parent in parents]

    @staticmethod
    def _get(parent_id, child_id):
        return CITypeRelation.get_by(parent_id=parent_id,
                                     child_id=child_id,
                                     to_dict=False,
                                     first=True)

    @staticmethod
    def acl_resource_name(first_name, second_name):
        return "{} -> {}".format(first_name, second_name)

    @classmethod
    def add(cls, parent, child, relation_type_id, constraint=ConstraintEnum.One2Many,
            parent_attr_id=None, child_attr_id=None):
        p = CITypeManager.check_is_existed(parent)
        c = CITypeManager.check_is_existed(child)

        rels = {}
        for i in CITypeRelation.get_by(to_dict=False):
            rels.setdefault(i.child_id, set()).add(i.parent_id)
        rels.setdefault(c.id, set()).add(p.id)

        try:
            toposort_flatten(rels)
        except toposort.CircularDependencyError as e:
            current_app.logger.warning(str(e))
            return abort(400, ErrFormat.circular_dependency_error)

        old_parent_attr_id = None
        existed = cls._get(p.id, c.id)
        if existed is not None:
            old_parent_attr_id = existed.parent_attr_id
            existed = existed.update(relation_type_id=relation_type_id,
                                     constraint=constraint,
                                     parent_attr_id=parent_attr_id,
                                     child_attr_id=child_attr_id,
                                     filter_none=False)
        else:
            existed = CITypeRelation.create(parent_id=p.id,
                                            child_id=c.id,
                                            relation_type_id=relation_type_id,
                                            parent_attr_id=parent_attr_id,
                                            child_attr_id=child_attr_id,
                                            constraint=constraint)

            if current_app.config.get("USE_ACL"):
                resource_name = cls.acl_resource_name(p.name, c.name)
                ACLManager().add_resource(resource_name, ResourceTypeEnum.CI_TYPE_RELATION)
                ACLManager().grant_resource_to_role(resource_name,
                                                    RoleEnum.CMDB_READ_ALL,
                                                    ResourceTypeEnum.CI_TYPE_RELATION,
                                                    permissions=[PermEnum.READ])
                ACLManager().grant_resource_to_role(resource_name,
                                                    current_user.username,
                                                    ResourceTypeEnum.CI_TYPE_RELATION)

        if parent_attr_id and parent_attr_id != old_parent_attr_id:
            if parent_attr_id and parent_attr_id != existed.parent_attr_id:
                from api.tasks.cmdb import rebuild_relation_for_attribute_changed
                rebuild_relation_for_attribute_changed.apply_async(args=(existed.to_dict()))

        CITypeHistoryManager.add(CITypeOperateType.ADD_RELATION, p.id,
                                 change=dict(parent=p.to_dict(), child=c.to_dict(), relation_type_id=relation_type_id))

        return existed.id

    @classmethod
    def delete(cls, _id):
        ctr = (CITypeRelation.get_by_id(_id) or
               abort(404, ErrFormat.ci_type_relation_not_found.format("id={}".format(_id))))
        ctr.soft_delete()

        CITypeHistoryManager.add(CITypeOperateType.DELETE_RELATION, ctr.parent_id,
                                 change=dict(parent_id=ctr.parent.to_dict(), child=ctr.child.to_dict(),
                                             relation_type_id=ctr.relation_type_id))

        if current_app.config.get("USE_ACL"):
            p = CITypeManager.check_is_existed(ctr.parent_id)
            c = CITypeManager.check_is_existed(ctr.child_id)

            resource_name = cls.acl_resource_name(p.name, c.name)
            ACLManager().del_resource(resource_name, ResourceTypeEnum.CI_TYPE_RELATION)

    @classmethod
    def delete_2(cls, parent, child):
        ctr = cls._get(parent, child)

        cls.delete(ctr.id)

    @staticmethod
    def get_level2constraint(root_id, level):
        level = level + 1 if level == 1 else level
        ci = CI.get_by_id(root_id)
        if ci is None:
            return dict()

        root_id = ci.type_id
        level2constraint = dict()
        for lv in range(1, int(level) + 1):
            for i in CITypeRelation.get_by(parent_id=root_id, to_dict=False):
                if i.constraint == ConstraintEnum.Many2Many:
                    root_id = i.child_id
                    level2constraint[lv] = ConstraintEnum.Many2Many
                    break

        return level2constraint


class CITypeAttributeGroupManager(object):
    cls = CITypeAttributeGroup

    @staticmethod
    def get_by_type_id(type_id, need_other=False):
        parent_ids = CITypeInheritanceManager.base(type_id)

        groups = []
        id2type = {i: CITypeCache.get(i).alias for i in parent_ids}
        for _type_id in parent_ids + [type_id]:
            _groups = CITypeAttributeGroup.get_by(type_id=_type_id)
            _groups = sorted(_groups, key=lambda x: x["order"] or 0)
            for i in _groups:
                if type_id != _type_id:
                    i['inherited'] = True
                    i['inherited_from'] = id2type[_type_id]
                else:
                    i['inherited'] = False

            groups.extend(_groups)

        grouped = set()

        attributes = CITypeAttributeManager.get_attributes_by_type_id(type_id)
        id2attr = {i.get('id'): i for i in attributes}

        group2pos = dict()
        attr2pos = dict()
        result = []
        for group in groups:
            items = CITypeAttributeGroupItem.get_by(group_id=group["id"], to_dict=False)
            items = sorted(items, key=lambda x: x.order or 0)

            if group['name'] not in group2pos:
                group_pos = len(result)
                group['attributes'] = []
                result.append(group)

                group2pos[group['name']] = group_pos
            else:
                group_pos = group2pos[group['name']]

            attr = None
            for i in items:
                if i.attr_id in id2attr:
                    attr = id2attr[i.attr_id]
                    attr['inherited'] = group['inherited']
                    attr['inherited_from'] = group.get('inherited_from')
                    result[group_pos]['attributes'].append(attr)

                if i.attr_id in attr2pos:
                    result[attr2pos[i.attr_id][0]]['attributes'].remove(attr2pos[i.attr_id][1])

                attr2pos[i.attr_id] = [group_pos, attr]

            group.pop('inherited_from', None)

            grouped |= set([i.attr_id for i in items])

        if need_other:
            grouped = set(grouped)
            other_attributes = [attr for attr in attributes if attr["id"] not in grouped]
            result.append(dict(attributes=other_attributes))

        return result

    @staticmethod
    def create_or_update(type_id, name, attr_order, group_order=0, is_update=False):
        """
        create or update
        :param type_id:
        :param name:
        :param group_order: group order
        :param attr_order:
        :param is_update:
        :return:
        """
        existed = CITypeAttributeGroup.get_by(type_id=type_id, name=name, first=True, to_dict=False)
        if existed and not attr_order and not is_update:
            return abort(400, ErrFormat.ci_type_attribute_group_duplicate.format(name))

        existed = existed or CITypeAttributeGroup.create(type_id=type_id, name=name, order=group_order)
        existed.update(order=group_order)
        attr_order = dict(attr_order)

        if attr_order:
            existed_items = CITypeAttributeGroupItem.get_by(group_id=existed.id, to_dict=False)
            for item in existed_items:
                if item.attr_id not in attr_order:
                    item.soft_delete()
                else:
                    item.update(order=attr_order[item.attr_id])

            existed_items = {item.attr_id: 1 for item in existed_items}
            for attr_id, order in attr_order.items():
                if attr_id not in existed_items:
                    CITypeAttributeGroupItem.create(group_id=existed.id, attr_id=attr_id, order=order)

        return existed

    @classmethod
    def update(cls, group_id, name, attr_order, group_order=0):
        group = CITypeAttributeGroup.get_by_id(group_id) or abort(404, "Group <{0}> does not exist".format(group_id))
        other = CITypeAttributeGroup.get_by(type_id=group.type_id, name=name, first=True, to_dict=False)
        if other is not None and other.id != group.id:
            return abort(400, ErrFormat.ci_type_attribute_group_duplicate.format(name))
        if name is not None:
            group.update(name=name)
        else:
            name = group.name

        cls.create_or_update(group.type_id, name, attr_order, group_order, is_update=True)

    @staticmethod
    def delete(group_id):
        group = (CITypeAttributeGroup.get_by_id(group_id) or
                 abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(group_id))))
        group.soft_delete()

        items = CITypeAttributeGroupItem.get_by(group_id=group_id, to_dict=False)
        for item in items:
            item.soft_delete()

        return group_id

    @classmethod
    def add_item(cls, group_id, attr_id, order):
        db.session.remove()

        existed = CITypeAttributeGroupItem.get_by(group_id=group_id,
                                                  attr_id=attr_id,
                                                  first=True,
                                                  to_dict=False)

        gt_items = db.session.query(CITypeAttributeGroupItem).filter(
            CITypeAttributeGroupItem.group_id == group_id).filter(
            CITypeAttributeGroupItem.deleted.is_(False)).filter(CITypeAttributeGroupItem.order >= order)
        for _item in gt_items:
            _order = _item.order
            _item.update(order=_order + 1)

        if existed is not None:
            existed.update(order=order)
        else:
            CITypeAttributeGroupItem.create(group_id=group_id, attr_id=attr_id, order=order)

    @classmethod
    def update_item(cls, group_id, attr_id, order):
        db.session.remove()

        existed = CITypeAttributeGroupItem.get_by(group_id=group_id,
                                                  attr_id=attr_id,
                                                  first=True,
                                                  to_dict=False)
        existed or abort(404, ErrFormat.ci_type_group_attribute_not_found.format(group_id, attr_id))

        if existed.order > order:  # forward, +1
            items = db.session.query(CITypeAttributeGroupItem).filter(
                CITypeAttributeGroupItem.deleted.is_(False)).filter(
                CITypeAttributeGroupItem.group_id == group_id).filter(
                CITypeAttributeGroupItem.order >= order).filter(
                CITypeAttributeGroupItem.order < existed.order)
            for item in items:
                item.update(order=item.order + 1)

        elif existed.order < order:  # backward, -1
            items = db.session.query(CITypeAttributeGroupItem).filter(
                CITypeAttributeGroupItem.deleted.is_(False)).filter(
                CITypeAttributeGroupItem.group_id == group_id).filter(
                CITypeAttributeGroupItem.order > existed.order).filter(
                CITypeAttributeGroupItem.order <= order)
            for item in items:
                item.update(order=item.order - 1)

        existed.update(order=order)

    @classmethod
    def delete_item(cls, group_id, attr_id):
        db.session.remove()

        item = CITypeAttributeGroupItem.get_by(group_id=group_id,
                                               attr_id=attr_id,
                                               first=True,
                                               to_dict=False)

        if item is not None:
            item.soft_delete()
            order = item.order
            gt_items = db.session.query(CITypeAttributeGroupItem).filter(
                CITypeAttributeGroupItem.deleted.is_(False)).filter(
                CITypeAttributeGroupItem.group_id == group_id).filter(CITypeAttributeGroupItem.order > order)
            for _item in gt_items:
                _order = _item.order
                _item.update(order=_order - 1)

    @classmethod
    def transfer(cls, type_id, _from, _to):
        current_app.logger.info("CIType[{0}] {1} -> {2}".format(type_id, _from, _to))
        if isinstance(_from, int):
            from_group = CITypeAttributeGroup.get_by_id(_from)
        else:
            from_group = CITypeAttributeGroup.get_by(name=_from, first=True, to_dict=False)
        from_group or abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(_from)))

        if isinstance(_to, int):
            to_group = CITypeAttributeGroup.get_by_id(_to)
        else:
            to_group = CITypeAttributeGroup.get_by(name=_to, first=True, to_dict=False)
        to_group or abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(_to)))

        from_order, to_order = from_group.order, to_group.order

        from_group.update(order=to_order)
        to_group.update(order=from_order)

        CITypeAttributesCache.clean(type_id)

        from api.tasks.cmdb import ci_type_attribute_order_rebuild
        ci_type_attribute_order_rebuild.apply_async(args=(type_id, current_user.uid), queue=CMDB_QUEUE)


class CITypeTemplateManager(object):
    @staticmethod
    def __import(cls, data, unique_key='name'):
        id2obj_dicts = {i[unique_key]: i for i in data}
        existed = cls.get_by(to_dict=False)
        id2existed = {getattr(i, unique_key): i for i in existed}
        existed_ids = [getattr(i, unique_key) for i in existed]

        id_map = dict()
        # add
        for added_id in set(id2obj_dicts.keys()) - set(existed_ids):
            _id = id2obj_dicts[added_id].pop('id', None)
            id2obj_dicts[added_id].pop('created_at', None)
            id2obj_dicts[added_id].pop('updated_at', None)
            id2obj_dicts[added_id].pop('uid', None)

            if cls == CIType:
                __id = CITypeManager.add(**id2obj_dicts[added_id])
                CITypeCache.clean(__id)
            elif cls == CITypeRelation:
                __id = CITypeRelationManager.add(id2obj_dicts[added_id].get('parent_id'),
                                                 id2obj_dicts[added_id].get('child_id'),
                                                 id2obj_dicts[added_id].get('relation_type_id'),
                                                 id2obj_dicts[added_id].get('constraint'),
                                                 id2obj_dicts[added_id].get('parent_attr_id'),
                                                 id2obj_dicts[added_id].get('child_attr_id'),
                                                 )
            else:
                obj = cls.create(flush=True, **id2obj_dicts[added_id])
                if cls == Attribute:
                    AttributeCache.clean(obj)
                __id = obj.id

            id_map[_id] = __id

        # update
        for updated_id in set(id2obj_dicts.keys()) & set(existed_ids):
            _id = id2obj_dicts[updated_id].pop('id', None)

            id2existed[updated_id].update(flush=True, **id2obj_dicts[updated_id])

            id_map[_id] = id2existed[updated_id].id

            if cls == Attribute:
                AttributeCache.clean(id2existed[updated_id])

            if cls == CIType:
                CITypeCache.clean(id2existed[updated_id].id)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

        return id_map

    def _import_attributes(self, type2attributes):
        attributes = [attr for type_id in type2attributes for attr in type2attributes[type_id]]
        attrs = []
        for i in copy.deepcopy(attributes):
            i.pop('default_show', None)
            i.pop('is_required', None)
            i.pop('order', None)
            i.pop('choice_web_hook', None)
            i.pop('choice_other', None)
            i.pop('order', None)
            i.pop('inherited', None)
            i.pop('inherited_from', None)
            choice_value = i.pop('choice_value', None)
            if not choice_value:
                i['is_choice'] = False

            attrs.append((i, choice_value))

        attr_id_map = self.__import(Attribute, [i[0] for i in copy.deepcopy(attrs)])

        for i, choice_value in attrs:
            if choice_value and not i.get('choice_web_hook') and not i.get('choice_other'):
                AttributeManager.add_choice_values(attr_id_map.get(i['id'], i['id']), i['value_type'], choice_value)

        return attr_id_map

    def _import_ci_types(self, ci_types, attr_id_map):
        for i in ci_types:
            i.pop("unique_key", None)
            i['unique_id'] = attr_id_map.get(i['unique_id'], i['unique_id'])
            i['uid'] = current_user.uid

        return self.__import(CIType, ci_types)

    def _import_ci_type_groups(self, ci_type_groups, type_id_map):
        _ci_type_groups = copy.deepcopy(ci_type_groups)
        for i in _ci_type_groups:
            i.pop('ci_types', None)

        group_id_map = self.__import(CITypeGroup, _ci_type_groups)

        # import group type items
        for group in ci_type_groups:
            for order, ci_type in enumerate(group.get('ci_types') or []):
                payload = dict(group_id=group_id_map.get(group['id'], group['id']),
                               type_id=type_id_map.get(ci_type['id'], ci_type['id']),
                               order=order)
                existed = CITypeGroupItem.get_by(group_id=payload['group_id'], type_id=payload['type_id'],
                                                 first=True, to_dict=False)
                if existed is None:
                    CITypeGroupItem.create(flush=True, **payload)
                else:
                    existed.update(flush=True, **payload)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def _import_relation_types(self, relation_types):
        return self.__import(RelationType, relation_types)

    @staticmethod
    def _import_ci_type_relations(ci_type_relations, type_id_map, relation_type_id_map):
        for i in ci_type_relations:
            i.pop('parent', None)
            i.pop('child', None)
            i.pop('relation_type', None)

            i['parent_id'] = type_id_map.get(i['parent_id'], i['parent_id'])
            i['child_id'] = type_id_map.get(i['child_id'], i['child_id'])
            i['relation_type_id'] = relation_type_id_map.get(i['relation_type_id'], i['relation_type_id'])

            try:
                CITypeRelationManager.add(i.get('parent_id'),
                                          i.get('child_id'),
                                          i.get('relation_type_id'),
                                          i.get('constraint'),
                                          )
            except BadRequest:
                pass

    @staticmethod
    def _import_type_attributes(type2attributes, type_id_map, attr_id_map):
        for type_id in type2attributes:
            CITypeAttributesCache.clean(type_id_map.get(int(type_id), type_id))

        for type_id in type2attributes:
            existed = CITypeAttributesCache.get2(type_id_map.get(int(type_id), type_id))
            existed_attr_names = {attr.name: ta for ta, attr in existed}

            handled = set()
            for attr in type2attributes[type_id]:
                payload = dict(type_id=type_id_map.get(int(type_id), type_id),
                               attr_id=attr_id_map.get(attr['id'], attr['id']),
                               default_show=attr['default_show'],
                               is_required=attr['is_required'],
                               order=attr['order'])
                if attr['name'] not in handled:
                    if attr['name'] not in existed_attr_names:  # new
                        CITypeAttribute.create(flush=True, **payload)
                    else:  # update
                        existed_attr_names[attr['name']].update(flush=True, **payload)

                    handled.add(attr['name'])

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

        for type_id in type2attributes:
            CITypeAttributesCache.clean(type_id_map.get(int(type_id), type_id))

    @staticmethod
    def _import_attribute_group(type2attribute_group, type_id_map, attr_id_map):
        for type_id in type2attribute_group:
            for group in type2attribute_group[type_id] or []:
                _group = copy.deepcopy(group)
                _group.pop('attributes', None)
                _group.pop('id', None)
                _group.pop('inherited', None)
                _group.pop('inherited_from', None)
                existed = CITypeAttributeGroup.get_by(name=_group['name'],
                                                      type_id=type_id_map.get(_group['type_id'], _group['type_id']),
                                                      first=True, to_dict=False)
                if existed is None:
                    _group['type_id'] = type_id_map.get(_group['type_id'], _group['type_id'])

                    existed = CITypeAttributeGroup.create(flush=True, **_group)

                for order, attr in enumerate(group['attributes'] or []):
                    item_existed = CITypeAttributeGroupItem.get_by(group_id=existed.id,
                                                                   attr_id=attr_id_map.get(attr['id'], attr['id']),
                                                                   first=True, to_dict=False)
                    if item_existed is None:
                        CITypeAttributeGroupItem.create(group_id=existed.id,
                                                        attr_id=attr_id_map.get(attr['id'], attr['id']),
                                                        order=order)
                    else:
                        item_existed.update(flush=True, order=order)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    @staticmethod
    def _import_auto_discovery_rules(rules):
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD

        for rule in rules:
            ci_type = CITypeCache.get(rule.pop('type_name', None))
            adr = rule.pop('adr', {}) or {}

            if ci_type:
                rule['type_id'] = ci_type.id
            if rule.get('adr_name'):
                ad_rule = AutoDiscoveryRuleCRUD.get_by_name(rule.pop("adr_name"))
                adr.pop('created_at', None)
                adr.pop('updated_at', None)
                adr.pop('id', None)

                if ad_rule:
                    rule['adr_id'] = ad_rule.id
                    ad_rule.update(**adr)

                elif adr:
                    ad_rule = AutoDiscoveryRuleCRUD().add(**adr)
                    rule['adr_id'] = ad_rule.id
                else:
                    continue

            rule.pop("id", None)
            rule.pop("created_at", None)
            rule.pop("updated_at", None)
            rule.pop("relation", None)

            rule['uid'] = current_user.uid

            if not rule.get('attributes'):
                continue

            existed = False
            for i in AutoDiscoveryCIType.get_by(type_id=ci_type.id, adr_id=rule['adr_id'], to_dict=False):
                if ((i.extra_option or {}).get('alias') or None) == (
                        (rule.get('extra_option') or {}).get('alias') or None):
                    existed = True
                    AutoDiscoveryCITypeCRUD().update(i.id, **rule)
                    break

            if not existed:
                try:
                    AutoDiscoveryCITypeCRUD().add(**rule)
                except Exception as e:
                    current_app.logger.warning("import auto discovery rules failed: {}".format(e))

    @staticmethod
    def _import_icons(icons):
        from api.lib.common_setting.upload_file import CommonFileCRUD
        for icon_name in icons:
            if icons[icon_name]:
                try:
                    CommonFileCRUD().save_str_to_file(icon_name, icons[icon_name])
                except Exception as e:
                    current_app.logger.warning("save icon failed: {}".format(e))

    def import_template(self, tpt):
        import time
        s = time.time()
        attr_id_map = self._import_attributes(tpt.get('type2attributes') or {})
        current_app.logger.info('import attributes cost: {}'.format(time.time() - s))

        s = time.time()
        ci_type_id_map = self._import_ci_types(tpt.get('ci_types') or [], attr_id_map)
        current_app.logger.info('import ci_types cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_ci_type_groups(tpt.get('ci_type_groups') or [], ci_type_id_map)
        current_app.logger.info('import ci_type_groups cost: {}'.format(time.time() - s))

        s = time.time()
        relation_type_id_map = self._import_relation_types(tpt.get('relation_types') or [])
        current_app.logger.info('import relation_types cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_ci_type_relations(tpt.get('ci_type_relations') or [], ci_type_id_map, relation_type_id_map)
        current_app.logger.info('import ci_type_relations cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_type_attributes(tpt.get('type2attributes') or {}, ci_type_id_map, attr_id_map)
        current_app.logger.info('import type2attributes cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_attribute_group(tpt.get('type2attribute_group') or {}, ci_type_id_map, attr_id_map)
        current_app.logger.info('import type2attribute_group cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_auto_discovery_rules(tpt.get('ci_type_auto_discovery_rules') or [])
        current_app.logger.info('import ci_type_auto_discovery_rules cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_icons(tpt.get('icons') or {})
        current_app.logger.info('import icons cost: {}'.format(time.time() - s))

    @staticmethod
    def export_template():
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD
        from api.lib.common_setting.upload_file import CommonFileCRUD

        tpt = dict(
            ci_types=CITypeManager.get_ci_types(),
            ci_type_groups=CITypeGroupManager.get(),
            relation_types=[i.to_dict() for i in RelationTypeManager.get_all()],
            ci_type_relations=CITypeRelationManager.get()[0],
            ci_type_auto_discovery_rules=list(),
            type2attributes=dict(),
            type2attribute_group=dict(),
            icons=dict()
        )

        def get_icon_value(icon):
            try:
                return CommonFileCRUD().get_file_binary_str(icon)
            except:
                return ""

        ad_rules = AutoDiscoveryCITypeCRUD.get_all()
        rules = []
        for r in ad_rules:
            r = r.to_dict()
            ci_type = CITypeCache.get(r.pop('type_id'))
            r['type_name'] = ci_type and ci_type.name
            if r.get('adr_id'):
                adr = AutoDiscoveryRuleCRUD.get_by_id(r.pop('adr_id'))
                r['adr_name'] = adr and adr.name
                r['adr'] = adr and adr.to_dict() or {}

                icon_url = r['adr'].get('option', {}).get('icon', {}).get('url')
                if icon_url and icon_url not in tpt['icons']:
                    tpt['icons'][icon_url] = get_icon_value(icon_url)

            rules.append(r)

        tpt['ci_type_auto_discovery_rules'] = rules

        for ci_type in tpt['ci_types']:
            if ci_type['icon'] and len(ci_type['icon'].split('$$')) > 3:
                icon_url = ci_type['icon'].split('$$')[3]
                if icon_url not in tpt['icons']:
                    tpt['icons'][icon_url] = get_icon_value(icon_url)

            tpt['type2attributes'][ci_type['id']] = CITypeAttributeManager.get_attributes_by_type_id(
                ci_type['id'], choice_web_hook_parse=False, choice_other_parse=False)

            for attr in tpt['type2attributes'][ci_type['id']]:
                for i in (attr.get('choice_value') or []):
                    if (i[1] or {}).get('icon', {}).get('url') and len(i[1]['icon']['url'].split('$$')) > 3:
                        icon_url = i[1]['icon']['url'].split('$$')[3]
                        if icon_url not in tpt['icons']:
                            tpt['icons'][icon_url] = get_icon_value(icon_url)

            tpt['type2attribute_group'][ci_type['id']] = CITypeAttributeGroupManager.get_by_type_id(ci_type['id'])

        return tpt

    @staticmethod
    def export_template_by_type(type_id):
        ci_type = CITypeCache.get(type_id) or abort(404, ErrFormat.ci_type_not_found2.format("id={}".format(type_id)))

        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD
        from api.lib.common_setting.upload_file import CommonFileCRUD

        tpt = dict(
            ci_types=CITypeManager.get_ci_types(type_name=ci_type.name, like=False),
            ci_type_auto_discovery_rules=list(),
            type2attributes=dict(),
            type2attribute_group=dict(),
            icons=dict()
        )

        def get_icon_value(icon):
            try:
                return CommonFileCRUD().get_file_binary_str(icon)
            except:
                return ""

        ad_rules = AutoDiscoveryCITypeCRUD.get_by_type_id(ci_type.id)
        rules = []
        for r in ad_rules:
            r = r.to_dict()
            r['type_name'] = ci_type and ci_type.name
            if r.get('adr_id'):
                adr = AutoDiscoveryRuleCRUD.get_by_id(r.pop('adr_id'))
                r['adr_name'] = adr and adr.name
                r['adr'] = adr and adr.to_dict() or {}

                icon_url = r['adr'].get('option', {}).get('icon', {}).get('url')
                if icon_url and icon_url not in tpt['icons']:
                    tpt['icons'][icon_url] = get_icon_value(icon_url)

            rules.append(r)
        tpt['ci_type_auto_discovery_rules'] = rules

        for ci_type in tpt['ci_types']:
            if ci_type['icon'] and len(ci_type['icon'].split('$$')) > 3:
                icon_url = ci_type['icon'].split('$$')[3]
                if icon_url not in tpt['icons']:
                    tpt['icons'][icon_url] = get_icon_value(icon_url)

            tpt['type2attributes'][ci_type['id']] = CITypeAttributeManager.get_attributes_by_type_id(
                ci_type['id'], choice_web_hook_parse=False, choice_other_parse=False)

            for attr in tpt['type2attributes'][ci_type['id']]:
                for i in (attr.get('choice_value') or []):
                    if (i[1] or {}).get('icon', {}).get('url') and len(i[1]['icon']['url'].split('$$')) > 3:
                        icon_url = i[1]['icon']['url'].split('$$')[3]
                        if icon_url not in tpt['icons']:
                            tpt['icons'][icon_url] = get_icon_value(icon_url)

            tpt['type2attribute_group'][ci_type['id']] = CITypeAttributeGroupManager.get_by_type_id(ci_type['id'])

        return tpt


class CITypeUniqueConstraintManager(object):
    @staticmethod
    def get_by_type_id(type_id):
        return CITypeUniqueConstraint.get_by(type_id=type_id, to_dict=False)

    @staticmethod
    def get_detail(type_id):
        res = CITypeUniqueConstraint.get_by(type_id=type_id, to_dict=False)
        result = []
        for constraint in res:
            attrs = [AttributeCache.get(i) for i in constraint.attr_ids]
            item = constraint.to_dict()
            item['attrs'] = [i.to_dict() for i in attrs if i]
            result.append(item)

        return result

    def add(self, type_id, attr_ids):
        for constraint in CITypeUniqueConstraint.get_by(type_id=type_id, to_dict=False):
            if set(constraint.attr_ids) == set(attr_ids):
                return abort(400, ErrFormat.unique_constraint_duplicate)

        for attr_id in set(attr_ids):
            attr = AttributeCache.get(attr_id)
            if attr.is_list or attr.value_type == ValueTypeEnum.JSON:
                return abort(400, ErrFormat.unique_constraint_invalid)

        new = CITypeUniqueConstraint.create(type_id=type_id, attr_ids=list(set(attr_ids)))

        CITypeHistoryManager.add(CITypeOperateType.ADD_UNIQUE_CONSTRAINT,
                                 type_id,
                                 unique_constraint_id=new.id, change=new.to_dict())

        return self.get_detail(type_id)

    def update(self, _id, attr_ids):
        existed = CITypeUniqueConstraint.get_by_id(_id) or abort(404, ErrFormat.not_found)

        for constraint in CITypeUniqueConstraint.get_by(type_id=existed.type_id, to_dict=False):
            if set(constraint.attr_ids) == set(attr_ids) and constraint.id != _id:
                return abort(400, ErrFormat.unique_constraint_duplicate)

        existed2 = existed.to_dict()
        if attr_ids != existed.attr_ids:
            new = existed.update(attr_ids=attr_ids)

            CITypeHistoryManager.add(CITypeOperateType.UPDATE_UNIQUE_CONSTRAINT,
                                     existed.type_id,
                                     unique_constraint_id=_id,
                                     change=dict(old=existed2, new=new.to_dict()))

        return self.get_detail(existed.type_id)

    @staticmethod
    def delete(_id):
        existed = CITypeUniqueConstraint.get_by_id(_id) or abort(404, ErrFormat.not_found)

        existed.soft_delete()

        CITypeHistoryManager.add(CITypeOperateType.DELETE_UNIQUE_CONSTRAINT,
                                 existed.type_id,
                                 unique_constraint_id=_id,
                                 change=existed.to_dict())


class CITypeTriggerManager(object):
    @staticmethod
    def get(type_id, to_dict=True):
        return CITypeTrigger.get_by(type_id=type_id, to_dict=to_dict)

    @staticmethod
    def add(type_id, attr_id, option):
        for i in CITypeTrigger.get_by(type_id=type_id, attr_id=attr_id, to_dict=False):
            if i.option == option:
                return abort(400, ErrFormat.ci_type_trigger_duplicate)

        not isinstance(option, dict) and abort(400, ErrFormat.argument_invalid.format("option"))

        trigger = CITypeTrigger.create(type_id=type_id, attr_id=attr_id, option=option)

        CITypeHistoryManager.add(CITypeOperateType.ADD_TRIGGER,
                                 type_id,
                                 trigger_id=trigger.id,
                                 change=trigger.to_dict())

        return trigger.to_dict()

    @staticmethod
    def update(_id, attr_id, option):
        existed = (CITypeTrigger.get_by_id(_id) or
                   abort(404, ErrFormat.ci_type_trigger_not_found.format("id={}".format(_id))))

        existed2 = existed.to_dict()
        new = existed.update(attr_id=attr_id or None, option=option, filter_none=False)

        CITypeHistoryManager.add(CITypeOperateType.UPDATE_TRIGGER,
                                 existed.type_id,
                                 trigger_id=_id,
                                 change=dict(old=existed2, new=new.to_dict()))

        return new.to_dict()

    @staticmethod
    def delete(_id):
        existed = (CITypeTrigger.get_by_id(_id) or
                   abort(404, ErrFormat.ci_type_trigger_not_found.format("id={}".format(_id))))

        existed.soft_delete()

        CITypeHistoryManager.add(CITypeOperateType.DELETE_TRIGGER,
                                 existed.type_id,
                                 trigger_id=_id,
                                 change=existed.to_dict())
