# -*- coding:utf-8 -*- 


from flask import current_app
from flask import abort

from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CIType
from api.models.cmdb import CITypeGroup
from api.models.cmdb import CITypeGroupItem
from api.models.cmdb import CITypeRelation
from api.models.cmdb import CITypeAttributeGroup
from api.models.cmdb import CITypeAttributeGroupItem
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.attribute import AttributeManager
from api.lib.decorator import kwargs_required


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

    @classmethod
    @kwargs_required("name")
    def add(cls, **kwargs):
        unique_key = kwargs.pop("unique_key", None)
        unique_key = AttributeCache.get(unique_key) or abort(404, "Unique key is not defined")

        CIType.get_by(name=kwargs['name'], first=True) and \
            abort(404, "CIType <{0}> is already existed".format(kwargs.get("name")))

        kwargs["alias"] = kwargs["name"] if not kwargs.get("alias") else kwargs["alias"]

        kwargs["unique_id"] = unique_key.id
        ci_type = CIType.create(**kwargs)

        CITypeAttributeManager.add(ci_type.id, [unique_key.id], is_required=True)

        CITypeCache.clean(ci_type.name)

        return ci_type.id

    @classmethod
    def update(cls, type_id, **kwargs):

        ci_type = cls.check_is_existed(type_id)

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
        ci_type.soft_delete()

        CITypeCache.clean(type_id)


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
        return [AttributeCache.get(attr.attr_id).name for attr in CITypeAttributeCache.get(type_id)]

    @staticmethod
    def get_attributes_by_type_id(type_id):
        attrs = CITypeAttributeCache.get(type_id)
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

        CITypeAttributeCache.clean(type_id)

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

        CITypeAttributeCache.clean(type_id)

    @classmethod
    def delete(cls, type_id, attr_ids=None):
        """
        delete attributes from CIType
        :param type_id: 
        :param attr_ids: list
        :return: 
        """
        cls._check(type_id, attr_ids)

        for attr_id in attr_ids:
            existed = CITypeAttribute.get_by(type_id=type_id,
                                             attr_id=attr_id,
                                             first=True,
                                             to_dict=False)
            if existed is not None:
                existed.soft_delete()

        CITypeAttributeCache.clean(type_id)


class CITypeRelationManager(object):
    """
    manage relation between CITypes
    """

    def __init__(self):
        pass

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
        existed = CITypeAttributeGroup.get_by(type_id=type_id, name=name, first=True, to_dict=False) \
            or CITypeAttributeGroup.create(type_id=type_id, name=name, order=group_order)
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
