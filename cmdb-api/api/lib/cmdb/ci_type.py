# -*- coding:utf-8 -*- 

import copy
import datetime

from flask import abort
from flask import current_app
from flask import g

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import CITypeOperateType
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import PermEnum, ResourceTypeEnum, RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.cmdb.history import CITypeHistoryManager
from api.lib.cmdb.relation_type import RelationTypeManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.models.cmdb import Attribute
from api.models.cmdb import CI
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeAttributeGroup
from api.models.cmdb import CITypeAttributeGroupItem
from api.models.cmdb import CITypeGroup
from api.models.cmdb import CITypeGroupItem
from api.models.cmdb import CITypeRelation
from api.models.cmdb import CITypeTrigger
from api.models.cmdb import CITypeUniqueConstraint
from api.models.cmdb import PreferenceRelationView
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

    @staticmethod
    def get_ci_types(type_name=None):
        resources = None
        if current_app.config.get('USE_ACL') and not is_app_admin():
            resources = set([i.get('name') for i in ACLManager().get_resources("CIType")])

        ci_types = CIType.get_by() if type_name is None else CIType.get_by_like(name=type_name)
        res = list()
        for type_dict in ci_types:
            type_dict["unique_key"] = AttributeCache.get(type_dict["unique_id"]).name
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
        from api.lib.cmdb.const import L_TYPE
        if L_TYPE and len(CIType.get_by()) > L_TYPE * 2:
            return abort(400, ErrFormat.limit_ci_type.format(L_TYPE * 2))

        unique_key = kwargs.pop("unique_key", None)
        unique_key = AttributeCache.get(unique_key) or abort(404, ErrFormat.unique_key_not_define)

        kwargs["alias"] = kwargs["name"] if not kwargs.get("alias") else kwargs["alias"]

        cls._validate_unique(name=kwargs['name'])
        cls._validate_unique(alias=kwargs['alias'])

        kwargs["unique_id"] = unique_key.id
        kwargs['uid'] = g.user.uid
        ci_type = CIType.create(**kwargs)

        CITypeAttributeManager.add(ci_type.id, [unique_key.id], is_required=True)

        CITypeCache.clean(ci_type.name)

        if current_app.config.get("USE_ACL"):
            ACLManager().add_resource(ci_type.name, ResourceTypeEnum.CI)
            ACLManager().grant_resource_to_role(ci_type.name,
                                                RoleEnum.CMDB_READ_ALL,
                                                ResourceTypeEnum.CI,
                                                permissions=[PermEnum.READ])
            ACLManager().grant_resource_to_role(ci_type.name,
                                                g.user.username,
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

        if ci_type.uid and ci_type.uid != g.user.uid:
            return abort(403, ErrFormat.only_owner_can_delete)

        if CI.get_by(type_id=type_id, first=True, to_dict=False) is not None:
            return abort(400, ErrFormat.ci_exists_and_cannot_delete_type)

        relation_views = PreferenceRelationView.get_by(to_dict=False)
        for rv in relation_views:
            for item in (rv.cr_ids or []):
                if item.get('parent_id') == type_id or item.get('child_id') == type_id:
                    return abort(400, ErrFormat.ci_relation_view_exists_and_cannot_delete_type.format(rv.name))

        for item in CITypeRelation.get_by(parent_id=type_id, to_dict=False):
            item.soft_delete()

        for item in CITypeRelation.get_by(child_id=type_id, to_dict=False):
            item.soft_delete()

        for item in PreferenceTreeView.get_by(type_id=type_id, to_dict=False):
            item.soft_delete()

        for item in PreferenceShowAttributes.get_by(type_id=type_id, to_dict=False):
            item.soft_delete()

        for item in CITypeGroupItem.get_by(type_id=type_id, to_dict=False):
            item.soft_delete()

        ci_type.soft_delete()

        CITypeCache.clean(type_id)

        CITypeHistoryManager.add(CITypeOperateType.DELETE, ci_type.id, change=ci_type.to_dict())

        if current_app.config.get("USE_ACL"):
            ACLManager().del_resource(ci_type.name, ResourceTypeEnum.CI)


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

        current_app.logger.info(resources)
        groups = sorted(CITypeGroup.get_by(), key=lambda x: x['order'] or 0)
        group_types = set()
        for group in groups:
            for t in sorted(CITypeGroupItem.get_by(group_id=group['id']), key=lambda x: x['order'] or 0):
                ci_type = CITypeCache.get(t['type_id']).to_dict()
                if resources is None or (ci_type and ci_type['name'] in resources):
                    ci_type['permissions'] = resources[ci_type['name']] if resources is not None else None
                    group.setdefault("ci_types", []).append(ci_type)
                    group_types.add(t["type_id"])

        if need_other:
            ci_types = CITypeManager.get_ci_types()
            other_types = dict(ci_types=[])
            for ci_type in ci_types:
                if ci_type["id"] not in group_types and (resources is None or ci_type['name'] in resources):
                    ci_type['permissions'] = resources.get(ci_type['name']) if resources is not None else None
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
        if name is not None:
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
    def get_attr_names_by_type_id(type_id):
        return [AttributeCache.get(attr.attr_id).name for attr in CITypeAttributesCache.get(type_id)]

    @staticmethod
    def get_attributes_by_type_id(type_id, choice_web_hook_parse=True):
        has_config_perm = ACLManager('cmdb').has_permission(
            CITypeManager.get_name_by_id(type_id), ResourceTypeEnum.CI, PermEnum.CONFIG)

        attrs = CITypeAttributesCache.get(type_id)
        result = list()
        for attr in sorted(attrs, key=lambda x: (x.order, x.id)):
            attr_dict = AttributeManager().get_attribute(attr.attr_id, choice_web_hook_parse)
            attr_dict["is_required"] = attr.is_required
            attr_dict["order"] = attr.order
            attr_dict["default_show"] = attr.default_show
            if not has_config_perm:
                attr_dict.pop('choice_web_hook', None)

            result.append(attr_dict)
        return result

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
                    AttributeValueManager.delete_attr_value(attr_id, ci.id)

                    ci_cache.apply_async([ci.id], queue=CMDB_QUEUE)

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
        order = _to.get('order')

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
        ci_type_attribute_order_rebuild.apply_async(args=(type_id,), queue=CMDB_QUEUE)


class CITypeRelationManager(object):
    """
    manage relation between CITypes
    """

    @staticmethod
    def get():
        res = CITypeRelation.get_by(to_dict=False)
        for idx, item in enumerate(res):
            _item = item.to_dict()
            res[idx] = _item
            res[idx]['parent'] = item.parent.to_dict()
            res[idx]['child'] = item.child.to_dict()
            res[idx]['relation_type'] = item.relation_type.to_dict()

        return res

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
        ci_type_dict["relation_type"] = relation_inst.relation_type.name
        ci_type_dict["constraint"] = relation_inst.constraint
        return ci_type_dict

    @classmethod
    def get_children(cls, parent_id):
        children = CITypeRelation.get_by(parent_id=parent_id, to_dict=False)

        return [cls._wrap_relation_type_dict(child.child_id, child) for child in children]

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
    def add(cls, parent, child, relation_type_id, constraint=ConstraintEnum.One2Many):
        p = CITypeManager.check_is_existed(parent)
        c = CITypeManager.check_is_existed(child)

        existed = cls._get(p.id, c.id)
        if existed is not None:
            existed.update(relation_type_id=relation_type_id,
                           constraint=constraint)
        else:
            existed = CITypeRelation.create(parent_id=p.id,
                                            child_id=c.id,
                                            relation_type_id=relation_type_id,
                                            constraint=constraint)

            if current_app.config.get("USE_ACL"):
                resource_name = cls.acl_resource_name(p.name, c.name)
                ACLManager().add_resource(resource_name, ResourceTypeEnum.CI_TYPE_RELATION)
                ACLManager().grant_resource_to_role(resource_name,
                                                    RoleEnum.CMDB_READ_ALL,
                                                    ResourceTypeEnum.CI_TYPE_RELATION,
                                                    permissions=[PermEnum.READ])
                ACLManager().grant_resource_to_role(resource_name,
                                                    g.user.username,
                                                    ResourceTypeEnum.CI_TYPE_RELATION)

        CITypeHistoryManager.add(CITypeOperateType.ADD_RELATION, p.id,
                                 change=dict(parent=p.to_dict(), child=c.to_dict(), relation_type_id=relation_type_id))

        return existed.id

    @classmethod
    def delete(cls, _id):
        ctr = CITypeRelation.get_by_id(_id) or \
              abort(404, ErrFormat.ci_type_relation_not_found.format("id={}".format(_id)))
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


class CITypeAttributeGroupManager(object):
    cls = CITypeAttributeGroup

    @staticmethod
    def get_by_type_id(type_id, need_other=False):
        groups = CITypeAttributeGroup.get_by(type_id=type_id)
        groups = sorted(groups, key=lambda x: x["order"] or 0)
        grouped = list()

        attributes = CITypeAttributeManager.get_attributes_by_type_id(type_id)
        id2attr = {i['id']: i for i in attributes}

        for group in groups:
            items = CITypeAttributeGroupItem.get_by(group_id=group["id"], to_dict=False)
            items = sorted(items, key=lambda x: x.order or 0)
            group["attributes"] = [id2attr.get(i.attr_id) for i in items if i.attr_id in id2attr]
            grouped.extend([i.attr_id for i in items])

        if need_other:
            grouped = set(grouped)
            other_attributes = [attr for attr in attributes if attr["id"] not in grouped]
            groups.append(dict(attributes=other_attributes))

        return groups

    @staticmethod
    def create_or_update(type_id, name, attr_order, group_order=0, is_update=False):
        """
        create or update
        :param type_id:
        :param name:
        :param group_order: group order
        :param attr_order:
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
        group = CITypeAttributeGroup.get_by_id(group_id) \
                or abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(group_id)))
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
        from_group = CITypeAttributeGroup.get_by_id(_from)
        from_group or abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(_from)))

        to_group = CITypeAttributeGroup.get_by_id(_to)
        to_group or abort(404, ErrFormat.ci_type_attribute_group_not_found.format("id={}".format(_to)))

        from_order, to_order = from_group.order, to_group.order

        from_group.update(order=to_order)
        to_group.update(order=from_order)

        CITypeAttributesCache.clean(type_id)

        from api.tasks.cmdb import ci_type_attribute_order_rebuild
        ci_type_attribute_order_rebuild.apply_async(args=(type_id,), queue=CMDB_QUEUE)


class CITypeTemplateManager(object):
    @staticmethod
    def __import(cls, data):
        id2obj_dicts = {i['id']: i for i in data}
        existed = cls.get_by(deleted=None, to_dict=False)
        id2existed = {i.id: i for i in existed}
        existed_ids = [i.id for i in existed]
        existed_no_delete_ids = [i.id for i in existed if not i.deleted]

        # add
        for added_id in set(id2obj_dicts.keys()) - set(existed_ids):
            if cls == CIType:
                CITypeManager.add(**id2obj_dicts[added_id])
            else:
                cls.create(flush=True, **id2obj_dicts[added_id])

        # update
        for updated_id in set(id2obj_dicts.keys()) & set(existed_ids):
            if cls == CIType:
                deleted = id2existed[updated_id].deleted
                CITypeManager.update(updated_id, **id2obj_dicts[updated_id])
                if deleted and current_app.config.get("USE_ACL"):
                    type_name = id2obj_dicts[updated_id]['name']
                    ACLManager().add_resource(type_name, ResourceTypeEnum.CI)
                    ACLManager().grant_resource_to_role(type_name,
                                                        RoleEnum.CMDB_READ_ALL,
                                                        ResourceTypeEnum.CI,
                                                        permissions=[PermEnum.READ])
                    ACLManager().grant_resource_to_role(type_name,
                                                        g.user.username,
                                                        ResourceTypeEnum.CI)

            else:
                id2existed[updated_id].update(flush=True, **id2obj_dicts[updated_id])

        # delete
        for deleted_id in set(existed_no_delete_ids) - set(id2obj_dicts.keys()):
            if cls == CIType:
                id2existed[deleted_id].soft_delete(flush=True)

                CITypeCache.clean(deleted_id)

                CITypeHistoryManager.add(CITypeOperateType.DELETE, deleted_id, change=id2existed[deleted_id].to_dict())

                if current_app.config.get("USE_ACL"):
                    ACLManager().del_resource(id2existed[deleted_id].name, ResourceTypeEnum.CI)
            else:
                id2existed[deleted_id].soft_delete(flush=True)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def _import_ci_types(self, ci_types):
        for i in ci_types:
            i.pop("unique_key", None)

        self.__import(CIType, ci_types)

    def _import_ci_type_groups(self, ci_type_groups):
        _ci_type_groups = copy.deepcopy(ci_type_groups)
        for i in _ci_type_groups:
            i.pop('ci_types', None)

        self.__import(CITypeGroup, _ci_type_groups)

        # import group type items
        for group in ci_type_groups:
            existed = CITypeGroupItem.get_by(group_id=group['id'], to_dict=False)
            for i in existed:
                i.soft_delete()

            for order, ci_type in enumerate(group.get('ci_types') or []):
                payload = dict(group_id=group['id'], type_id=ci_type['id'], order=order)
                CITypeGroupItem.create(**payload)

    def _import_relation_types(self, relation_types):
        self.__import(RelationType, relation_types)

    def _import_ci_type_relations(self, ci_type_relations):
        for i in ci_type_relations:
            i.pop('parent', None)
            i.pop('child', None)
            i.pop('relation_type', None)

        self.__import(CITypeRelation, ci_type_relations)

    def _import_attributes(self, type2attributes):
        attributes = [attr for type_id in type2attributes for attr in type2attributes[type_id]]
        attrs = []
        for i in copy.deepcopy(attributes):
            i.pop('default_show', None)
            i.pop('is_required', None)
            i.pop('order', None)
            choice_value = i.pop('choice_value', None)

            attrs.append((i, choice_value))

        self.__import(Attribute, [i[0] for i in attrs])

        for i, choice_value in attrs:
            if choice_value:
                AttributeManager.add_choice_values(i['id'], i['value_type'], choice_value)

    @staticmethod
    def _import_type_attributes(type2attributes):
        # add type attribute

        for type_id in type2attributes:
            existed = CITypeAttribute.get_by(type_id=type_id, to_dict=False)
            existed_attr_ids = {i.attr_id: i for i in existed}
            new_attr_ids = {i['id']: i for i in type2attributes[type_id]}

            for attr in type2attributes[type_id]:
                payload = dict(type_id=type_id,
                               attr_id=attr['id'],
                               default_show=attr['default_show'],
                               is_required=attr['is_required'],
                               order=attr['order'])
                if attr['id'] not in existed_attr_ids:  # new
                    CITypeAttribute.create(flush=True, **payload)
                else:  # update
                    existed_attr_ids[attr['id']].update(**payload)

            # delete
            for i in existed:
                if i.attr_id not in new_attr_ids:
                    i.soft_delete()

    @staticmethod
    def _import_attribute_group(type2attribute_group):
        for type_id in type2attribute_group:
            existed = CITypeAttributeGroup.get_by(type_id=type_id, to_dict=False)
            for i in existed:
                i.soft_delete()

            for group in type2attribute_group[type_id] or []:
                _group = copy.deepcopy(group)
                _group.pop('attributes', None)
                _group.pop('id', None)
                new = CITypeAttributeGroup.create(**_group)

                existed = CITypeAttributeGroupItem.get_by(group_id=new.id, to_dict=False)
                for i in existed:
                    i.soft_delete()

                for order, attr in enumerate(group['attributes'] or []):
                    CITypeAttributeGroupItem.create(group_id=new.id, attr_id=attr['id'], order=order)

    @staticmethod
    def _import_auto_discovery_rules(rules):
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD
        for rule in rules:
            ci_type = CITypeCache.get(rule.pop('type_name', None))
            if ci_type:
                rule['type_id'] = ci_type.id
            if rule.get('adr_name'):
                ad_rule = AutoDiscoveryRuleCRUD.get_by_name(rule.pop("adr_name"))
                if ad_rule:
                    rule['adr_id'] = ad_rule.id

            rule.pop("id", None)
            rule.pop("created_at", None)
            rule.pop("updated_at", None)

            rule['uid'] = g.user.uid
            try:
                AutoDiscoveryCITypeCRUD.add(**rule)
            except:
                pass

    def import_template(self, tpt):
        import time
        s = time.time()
        self._import_attributes(tpt.get('type2attributes') or {})
        current_app.logger.info('import attributes cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_ci_types(tpt.get('ci_types') or [])
        current_app.logger.info('import ci_types cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_ci_type_groups(tpt.get('ci_type_groups') or [])
        current_app.logger.info('import ci_type_groups cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_relation_types(tpt.get('relation_types') or [])
        current_app.logger.info('import relation_types cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_ci_type_relations(tpt.get('ci_type_relations') or [])
        current_app.logger.info('import ci_type_relations cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_type_attributes(tpt.get('type2attributes') or {})
        current_app.logger.info('import type2attributes cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_attribute_group(tpt.get('type2attribute_group') or {})
        current_app.logger.info('import type2attribute_group cost: {}'.format(time.time() - s))

        s = time.time()
        self._import_auto_discovery_rules(tpt.get('ci_type_auto_discovery_rules') or [])
        current_app.logger.info('import ci_type_auto_discovery_rules cost: {}'.format(time.time() - s))

    @staticmethod
    def export_template():
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryCITypeCRUD
        from api.lib.cmdb.auto_discovery.auto_discovery import AutoDiscoveryRuleCRUD

        ad_rules = AutoDiscoveryCITypeCRUD.get_all()
        rules = []
        for r in ad_rules:
            r = r.to_dict()
            ci_type = CITypeCache.get(r.pop('type_id'))
            r['type_name'] = ci_type and ci_type.name
            if r.get('adr_id'):
                adr = AutoDiscoveryRuleCRUD.get_by_id(r.pop('adr_id'))
                r['adr_name'] = adr and adr.name

            rules.append(r)

        tpt = dict(
            ci_types=CITypeManager.get_ci_types(),
            ci_type_groups=CITypeGroupManager.get(),
            relation_types=[i.to_dict() for i in RelationTypeManager.get_all()],
            ci_type_relations=CITypeRelationManager.get(),
            ci_type_auto_discovery_rules=rules,
            type2attributes=dict(),
            type2attribute_group=dict()
        )

        for ci_type in tpt['ci_types']:
            tpt['type2attributes'][ci_type['id']] = CITypeAttributeManager.get_attributes_by_type_id(
                ci_type['id'], choice_web_hook_parse=False)

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
    def get(type_id):
        return CITypeTrigger.get_by(type_id=type_id, to_dict=True)

    @staticmethod
    def add(type_id, attr_id, notify):
        CITypeTrigger.get_by(type_id=type_id, attr_id=attr_id) and abort(400, ErrFormat.ci_type_trigger_duplicate)

        not isinstance(notify, dict) and abort(400, ErrFormat.argument_invalid.format("notify"))

        trigger = CITypeTrigger.create(type_id=type_id, attr_id=attr_id, notify=notify)

        CITypeHistoryManager.add(CITypeOperateType.ADD_TRIGGER,
                                 type_id,
                                 trigger_id=trigger.id,
                                 change=trigger.to_dict())

        return trigger.to_dict()

    @staticmethod
    def update(_id, notify):
        existed = CITypeTrigger.get_by_id(_id) or \
                  abort(404, ErrFormat.ci_type_trigger_not_found.format("id={}".format(_id)))

        existed2 = existed.to_dict()
        new = existed.update(notify=notify)

        CITypeHistoryManager.add(CITypeOperateType.UPDATE_TRIGGER,
                                 existed.type_id,
                                 trigger_id=_id,
                                 change=dict(old=existed2, new=new.to_dict()))

        return new.to_dict()

    @staticmethod
    def delete(_id):
        existed = CITypeTrigger.get_by_id(_id) or \
                  abort(404, ErrFormat.ci_type_trigger_not_found.format("id={}".format(_id)))

        existed.soft_delete()

        CITypeHistoryManager.add(CITypeOperateType.DELETE_TRIGGER,
                                 existed.type_id,
                                 trigger_id=_id,
                                 change=existed.to_dict())

    @staticmethod
    def waiting_cis(trigger):
        now = datetime.datetime.today()

        delta_time = datetime.timedelta(days=(trigger.notify.get('before_days', 0) or 0))

        attr = AttributeCache.get(trigger.attr_id)

        value_table = TableMap(attr=attr).table

        values = value_table.get_by(attr_id=attr.id, to_dict=False)

        result = []
        for v in values:
            if isinstance(v.value, (datetime.date, datetime.datetime)) and \
                    (v.value - delta_time).strftime('%Y%m%d') == now.strftime("%Y%m%d"):
                result.append(v)

        return result

    @staticmethod
    def trigger_notify(trigger, ci):
        if trigger.notify.get('notify_at') == datetime.datetime.now().strftime("%H:%M") or \
                not trigger.notify.get('notify_at'):
            from api.tasks.cmdb import trigger_notify

            trigger_notify.apply_async(args=(trigger.notify, ci.ci_id), queue=CMDB_QUEUE)

            return True

        return False
