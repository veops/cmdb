# -*- coding:utf-8 -*- 


from flask import abort
from flask import current_app

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.models.cmdb import CI
from api.models.cmdb import CIType
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeAttributeGroup
from api.models.cmdb import CITypeAttributeGroupItem
from api.models.cmdb import CITypeGroup
from api.models.cmdb import CITypeGroupItem
from api.models.cmdb import CITypeRelation
from api.models.cmdb import PreferenceShowAttributes
from api.models.cmdb import PreferenceTreeView
from api.tasks.cmdb import ci_type_attribute_order_rebuild


class CITypeManager(object):
    """
    manage CIType
    """

    def __init__(self):
        pass

    @staticmethod
    def get_name_by_id(type_id):
        return CITypeCache.get(type_id).name

    @staticmethod
    def check_is_existed(key):
        return CITypeCache.get(key) or abort(404, "CIType <{0}> is not existed".format(key))

    @staticmethod
    def get_ci_types(type_name=None):
        ci_types = CIType.get_by() if type_name is None else CIType.get_by_like(name=type_name)
        res = list()
        for type_dict in ci_types:
            type_dict["unique_key"] = AttributeCache.get(type_dict["unique_id"]).name
            res.append(type_dict)
        return res

    @staticmethod
    def query(_type):
        ci_type = CITypeCache.get(_type) or abort(404, "CIType <{0}> is not found".format(_type))
        return ci_type.to_dict()

    @staticmethod
    def _validate_unique(type_id=None, name=None, alias=None):
        if name is not None:
            ci_type = CIType.get_by(name=name, first=True, to_dict=False)
        elif alias is not None:
            ci_type = CIType.get_by(alias=alias, first=True, to_dict=False)
        else:
            return

        if type_id is not None and ci_type.id != type_id:
            return abort(400, "CIType <{0}> is already existed".format(name or alias))

        if type_id is None and ci_type is not None:
            return abort(400, "CIType <{0}> is already existed".format(name or alias))

    @classmethod
    @kwargs_required("name")
    def add(cls, **kwargs):
        unique_key = kwargs.pop("unique_key", None)
        unique_key = AttributeCache.get(unique_key) or abort(404, "Unique key is not defined")

        kwargs["alias"] = kwargs["name"] if not kwargs.get("alias") else kwargs["alias"]

        cls._validate_unique(name=kwargs['name'])
        cls._validate_unique(alias=kwargs['alias'])

        kwargs["unique_id"] = unique_key.id
        ci_type = CIType.create(**kwargs)

        CITypeAttributeManager.add(ci_type.id, [unique_key.id], is_required=True)

        CITypeCache.clean(ci_type.name)

        if current_app.config.get("USE_ACL"):
            from api.lib.perm.acl.acl import ACLManager
            from api.lib.cmdb.const import ResourceTypeEnum, RoleEnum, PermEnum
            ACLManager().add_resource(ci_type.name, ResourceTypeEnum.CI)
            ACLManager().grant_resource_to_role(ci_type.name,
                                                RoleEnum.CMDB_READ_ALL,
                                                ResourceTypeEnum.CI,
                                                permissions=[PermEnum.READ])

        return ci_type.id

    @classmethod
    def update(cls, type_id, **kwargs):

        ci_type = cls.check_is_existed(type_id)

        cls._validate_unique(type_id=type_id, name=kwargs.get('name'))
        cls._validate_unique(type_id=type_id, alias=kwargs.get('alias'))

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

        ci_type.update(**kwargs)

        CITypeCache.clean(type_id)

        return type_id

    @classmethod
    def set_enabled(cls, type_id, enabled=True):
        ci_type = cls.check_is_existed(type_id)
        ci_type.update(enabled=enabled)
        return type_id

    @classmethod
    def delete(cls, type_id):
        ci_type = cls.check_is_existed(type_id)

        if CI.get_by(type_id=type_id, first=True, to_dict=False) is not None:
            return abort(400, "cannot delete, because CI instance exists")

        for item in CITypeRelation.get_by(parent_id=type_id, to_dict=False):
            item.soft_delete()

        for item in CITypeRelation.get_by(child_id=type_id, to_dict=False):
            item.soft_delete()

        for item in PreferenceTreeView.get_by(type_id=type_id, to_dict=False):
            item.soft_delete()

        for item in PreferenceShowAttributes.get_by(type_id=type_id, to_dict=False):
            item.soft_delete()

        ci_type.soft_delete()

        CITypeCache.clean(type_id)

        if current_app.config.get("USE_ACL"):
            from api.lib.perm.acl.acl import ACLManager
            from api.lib.cmdb.const import ResourceTypeEnum, RoleEnum, PermEnum
            ACLManager().del_resource(ci_type.name, ResourceTypeEnum.CI)


class CITypeGroupManager(object):
    @staticmethod
    def get(need_other=None):
        groups = CITypeGroup.get_by()
        group_types = set()
        for group in groups:
            for t in sorted(CITypeGroupItem.get_by(group_id=group['id']), key=lambda x: x['order']):
                group.setdefault("ci_types", []).append(CITypeCache.get(t['type_id']).to_dict())
                group_types.add(t["type_id"])

        if need_other:
            ci_types = CITypeManager.get_ci_types()
            other_types = dict(ci_types=[ci_type for ci_type in ci_types if ci_type["id"] not in group_types])
            groups.append(other_types)

        return groups

    @staticmethod
    def add(name):
        CITypeGroup.get_by(name=name, first=True) and abort(400, "Group {0} does exist".format(name))
        return CITypeGroup.create(name=name)

    @staticmethod
    def update(gid, name, type_ids):
        """
        update all
        :param gid: 
        :param name: 
        :param type_ids: 
        :return: 
        """
        existed = CITypeGroup.get_by_id(gid) or abort(404, "Group <{0}> does not exist".format(gid))
        if name is not None:
            existed.update(name=name)

        for idx, type_id in enumerate(type_ids):

            item = CITypeGroupItem.get_by(group_id=gid, type_id=type_id, first=True, to_dict=False)
            if item is not None:
                item.update(order=idx)
            else:
                CITypeGroupItem.create(group_id=gid, type_id=type_id, order=idx)

    @staticmethod
    def delete(gid):
        existed = CITypeGroup.get_by_id(gid) or abort(404, "Group <{0}> does not exist".format(gid))

        items = CITypeGroupItem.get_by(group_id=gid, to_dict=False)
        for item in items:
            item.soft_delete()

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
    def get_attributes_by_type_id(type_id):
        attrs = CITypeAttributesCache.get(type_id)
        result = list()
        for attr in sorted(attrs, key=lambda x: (x.order, x.id)):
            attr_dict = AttributeManager().get_attribute(attr.attr_id)
            attr_dict["is_required"] = attr.is_required
            attr_dict["order"] = attr.order
            attr_dict["default_show"] = attr.default_show
            result.append(attr_dict)
        return result

    @staticmethod
    def _check(type_id, attr_ids):
        CITypeManager.check_is_existed(type_id)

        if not attr_ids or not isinstance(attr_ids, list):
            return abort(400, "Attributes are required")

        for attr_id in attr_ids:
            AttributeCache.get(attr_id) or abort(404, "Attribute <{0}> is not existed".format(attr_id))

    @classmethod
    def add(cls, type_id, attr_ids=None, **kwargs):
        """
        add attributes to CIType
        :param type_id: 
        :param attr_ids: list
        :param kwargs: 
        :return: 
        """
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

            existed.update(**attr)

            CITypeAttributeCache.clean(type_id, existed.attr_id)

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

        cls._check(type_id, attr_ids)

        for attr_id in attr_ids:
            existed = CITypeAttribute.get_by(type_id=type_id,
                                             attr_id=attr_id,
                                             first=True,
                                             to_dict=False)
            if existed is not None:
                existed.soft_delete()

                for ci in CI.get_by(type_id=type_id, to_dict=False):
                    AttributeValueManager.delete_attr_value(attr_id, ci.id)

                    ci_cache.apply_async([ci.id], queue=CMDB_QUEUE)

                CITypeAttributeCache.clean(type_id, attr_id)

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
            return abort(400, "invalid operation!!!")

        CITypeAttributesCache.clean(type_id)

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
    def _wrap_relation_type_dict(type_id, relation_inst):
        ci_type_dict = CITypeCache.get(type_id).to_dict()
        ci_type_dict["ctr_id"] = relation_inst.id
        ci_type_dict["attributes"] = CITypeAttributeManager.get_attributes_by_type_id(ci_type_dict["id"])
        ci_type_dict["relation_type"] = relation_inst.relation_type.name
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

    @classmethod
    def add(cls, parent, child, relation_type_id):
        p = CITypeManager.check_is_existed(parent)
        c = CITypeManager.check_is_existed(child)

        existed = cls._get(p.id, c.id)
        if existed is not None:
            existed.update(relation_type_id=relation_type_id)
        else:
            existed = CITypeRelation.create(parent_id=p.id,
                                            child_id=c.id,
                                            relation_type_id=relation_type_id)
        return existed.id

    @staticmethod
    def delete(_id):
        ctr = CITypeRelation.get_by_id(_id) or abort(404, "Type relation <{0}> is not found".format(_id))
        ctr.soft_delete()

    @classmethod
    def delete_2(cls, parent, child):
        ctr = cls._get(parent, child)
        return cls.delete(ctr.id)


class CITypeAttributeGroupManager(object):
    @staticmethod
    def get_by_type_id(type_id, need_other=None):
        groups = CITypeAttributeGroup.get_by(type_id=type_id)
        groups = sorted(groups, key=lambda x: x["order"])
        grouped = list()
        for group in groups:
            items = CITypeAttributeGroupItem.get_by(group_id=group["id"], to_dict=False)
            items = sorted(items, key=lambda x: x.order)
            group["attributes"] = [AttributeCache.get(i.attr_id).to_dict() for i in items]
            grouped.extend([i.attr_id for i in items])

        if need_other is not None:
            grouped = set(grouped)
            attributes = CITypeAttributeManager.get_attributes_by_type_id(type_id)
            other_attributes = [attr for attr in attributes if attr["id"] not in grouped]
            groups.append(dict(attributes=other_attributes))

        return groups

    @staticmethod
    def create_or_update(type_id, name, attr_order, group_order=0):
        """
        create or update
        :param type_id:
        :param name:
        :param group_order: group order
        :param attr_order:
        :return:
        """
        existed = CITypeAttributeGroup.get_by(type_id=type_id, name=name, first=True, to_dict=False)
        existed = existed or CITypeAttributeGroup.create(type_id=type_id, name=name, order=group_order)
        existed.update(order=group_order)
        attr_order = dict(attr_order)
        current_app.logger.info(attr_order)
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
            return abort(400, "Group <{0}> duplicate".format(name))
        if name is not None:
            group.update(name=name)

        cls.create_or_update(group.type_id, name, attr_order, group_order)

    @staticmethod
    def delete(group_id):
        group = CITypeAttributeGroup.get_by_id(group_id) \
                or abort(404, "AttributeGroup <{0}> does not exist".format(group_id))
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
        if existed is not None:
            existed.update(order=order)
        else:
            CITypeAttributeGroupItem.create(group_id=group_id, attr_id=attr_id, order=order)

        gt_items = db.session.query(CITypeAttributeGroupItem).filter(
            CITypeAttributeGroupItem.deleted.is_(False)).filter(CITypeAttributeGroupItem.order > order)
        for _item in gt_items:
            _order = _item.order
            _item.update(order=_order + 1)

    @classmethod
    def update_item(cls, group_id, attr_id, order):
        db.session.remove()

        existed = CITypeAttributeGroupItem.get_by(group_id=group_id,
                                                  attr_id=attr_id,
                                                  first=True,
                                                  to_dict=False)
        existed or abort(404, "Group<{0}> - Attribute<{1}> is not found".format(group_id, attr_id))

        if existed.order > order:  # forward, +1
            items = db.session.query(CITypeAttributeGroupItem).filter(
                CITypeAttributeGroupItem.deleted.is_(False)).filter(
                CITypeAttributeGroupItem.order >= order).filter(
                CITypeAttributeGroupItem.order < existed.order)
            for item in items:
                item.update(order=item.order + 1)

        elif existed.order < order:  # backward, -1
            items = db.session.query(CITypeAttributeGroupItem).filter(
                CITypeAttributeGroupItem.deleted.is_(False)).filter(
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
                CITypeAttributeGroupItem.deleted.is_(False)).filter(CITypeAttributeGroupItem.order > order)
            for _item in gt_items:
                _order = _item.order
                _item.update(order=_order - 1)

    @classmethod
    def transfer(cls, type_id, _from, _to):
        current_app.logger.info("CIType[{0}] {1} -> {2}".format(type_id, _from, _to))
        from_group = CITypeAttributeGroup.get_by_id(_from)
        from_group or abort(404, "Group <{0}> is not found".format(_from))

        to_group = CITypeAttributeGroup.get_by_id(_to)
        to_group or abort(404, "Group <{0}> is not found".format(_to))

        from_order, to_order = from_group.order, to_group.order

        from_group.update(order=to_order)
        to_group.update(order=from_order)

        CITypeAttributesCache.clean(type_id)

        ci_type_attribute_order_rebuild.apply_async(args=(type_id,), queue=CMDB_QUEUE)
