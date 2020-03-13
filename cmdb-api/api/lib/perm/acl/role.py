# -*- coding:utf-8 -*-


import six
from flask import abort

from api.extensions import db
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import RoleRelationCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.models.acl import Resource
from api.models.acl import ResourceGroupItems
from api.models.acl import ResourceType
from api.models.acl import Role
from api.models.acl import RolePermission
from api.models.acl import RoleRelation
from api.tasks.acl import role_rebuild


class RoleRelationCRUD(object):
    @staticmethod
    def get_parents(rids=None, uids=None):
        rid2uid = dict()
        if uids is not None:
            uids = [uids] if isinstance(uids, six.integer_types) else uids
            rids = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.in_(uids))
            rid2uid = {i.id: i.uid for i in rids}
            rids = [i.id for i in rids]
        else:
            rids = [rids] if isinstance(rids, six.integer_types) else rids

        res = db.session.query(RoleRelation).filter(
            RoleRelation.child_id.in_(rids)).filter(RoleRelation.deleted.is_(False))
        id2parents = {}
        for i in res:
            id2parents.setdefault(rid2uid.get(i.child_id, i.child_id), []).append(RoleCache.get(i.parent_id).to_dict())

        return id2parents

    @staticmethod
    def get_parent_ids(rid):
        res = RoleRelation.get_by(child_id=rid, to_dict=False)

        return [i.parent_id for i in res]

    @staticmethod
    def get_child_ids(rid):
        res = RoleRelation.get_by(parent_id=rid, to_dict=False)

        return [i.child_id for i in res]

    @classmethod
    def recursive_parent_ids(cls, rid):
        all_parent_ids = set()

        def _get_parent(_id):
            all_parent_ids.add(_id)
            parent_ids = RoleRelationCache.get_parent_ids(_id)
            for parent_id in parent_ids:
                _get_parent(parent_id)

        _get_parent(rid)

        return all_parent_ids

    @classmethod
    def recursive_child_ids(cls, rid):
        all_child_ids = set()

        def _get_children(_id):
            all_child_ids.add(_id)
            child_ids = RoleRelationCache.get_child_ids(_id)
            for child_id in child_ids:
                _get_children(child_id)

        _get_children(rid)

        return all_child_ids

    @classmethod
    def add(cls, parent_id, child_id):
        RoleRelation.get_by(parent_id=parent_id, child_id=child_id) and abort(400, "It's already existed")

        if parent_id in cls.recursive_child_ids(child_id):
            return abort(400, "Circulation inheritance!!!")

        RoleRelationCache.clean(parent_id)
        RoleRelationCache.clean(child_id)

        return RoleRelation.create(parent_id=parent_id, child_id=child_id)

    @classmethod
    def delete(cls, _id):
        existed = RoleRelation.get_by_id(_id) or abort(400, "RoleRelation <{0}> does not exist".format(_id))

        child_ids = cls.recursive_child_ids(existed.child_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id,), queue=ACL_QUEUE)

        RoleRelationCache.clean(existed.parent_id)
        RoleRelationCache.clean(existed.child_id)

        existed.soft_delete()

    @classmethod
    def delete2(cls, parent_id, child_id):
        existed = RoleRelation.get_by(parent_id=parent_id, child_id=child_id, first=True, to_dict=False)
        existed or abort(400, "RoleRelation < {0} -> {1} > does not exist".format(parent_id, child_id))

        child_ids = cls.recursive_child_ids(existed.child_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id,), queue=ACL_QUEUE)

        RoleRelationCache.clean(existed.parent_id)
        RoleRelationCache.clean(existed.child_id)

        existed.soft_delete()


class RoleCRUD(object):
    @staticmethod
    def search(q, app_id, page=1, page_size=None, user_role=True):
        query = db.session.query(Role).filter(Role.deleted.is_(False))
        query = query.filter(Role.app_id == app_id).filter(Role.uid.is_(None))

        if user_role:
            query1 = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.isnot(None))
            query = query.union(query1)

        if q:
            query = query.filter(Role.name.ilike('%{0}%'.format(q)))

        numfound = query.count()

        return numfound, query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def add_role(name, app_id=None, is_app_admin=False, uid=None):
        Role.get_by(name=name, app_id=app_id) and abort(400, "Role <{0}> is already existed".format(name))

        return Role.create(name=name,
                           app_id=app_id,
                           is_app_admin=is_app_admin,
                           uid=uid)

    @staticmethod
    def update_role(rid, **kwargs):
        kwargs.pop('app_id', None)

        role = Role.get_by_id(rid) or abort(404, "Role <{0}> does not exist".format(rid))

        RoleCache.clean(rid)

        return role.update(**kwargs)

    @classmethod
    def delete_role(cls, rid):
        role = Role.get_by_id(rid) or abort(404, "Role <{0}> does not exist".format(rid))

        for i in RoleRelation.get_by(parent_id=rid, to_dict=False):
            i.soft_delete()
        for i in RoleRelation.get_by(child_id=rid, to_dict=False):
            i.soft_delete()

        for i in RolePermission.get_by(rid=rid, to_dict=False):
            i.soft_delete()

        role_rebuild.apply_async(args=(list(RoleRelationCRUD.recursive_child_ids(rid)), ), queue=ACL_QUEUE)

        RoleCache.clean(rid)
        RoleRelationCache.clean(rid)

        role.soft_delete()

    @staticmethod
    def get_resources(rid):
        res = RolePermission.get_by(rid=rid, to_dict=False)
        id2perms = dict(id2perms={}, group2perms={})
        for i in res:
            if i.resource_id:
                id2perms['id2perms'].setdefault(i.resource_id, []).append(i.perm.name)
            elif i.group_id:
                id2perms['group2perms'].setdefault(i.group_id, []).append(i.perm.name)

        return id2perms

    @staticmethod
    def get_group_ids(resource_id):
        return [i.group_id for i in ResourceGroupItems.get_by(resource_id=resource_id, to_dict=False)]

    @classmethod
    def has_permission(cls, rid, resource_name, resource_type, app_id, perm):
        resource_type = ResourceType.get_by(app_id=app_id, name=resource_type, first=True, to_dict=False)
        resource_type or abort(404, "ResourceType <{0}> is not found".format(resource_type))
        type_id = resource_type.id
        resource = Resource.get_by(name=resource_name, resource_type_id=type_id, first=True, to_dict=False)
        resource = resource or abort(403, "Resource <{0}> is not in ACL".format(resource_name))

        parent_ids = RoleRelationCRUD.recursive_parent_ids(rid)

        group_ids = cls.get_group_ids(resource.id)
        for parent_id in parent_ids:
            id2perms = RoleRelationCache.get_resources(parent_id)
            perms = id2perms['id2perms'].get(resource.id, [])
            if perms and {perm}.issubset(set(perms)):
                return True

            for group_id in group_ids:
                perms = id2perms['group2perms'].get(group_id, [])
                if perms and {perm}.issubset(set(perms)):
                    return True

        return False

    @classmethod
    def get_permissions(cls, rid, resource_name):
        resource = Resource.get_by(name=resource_name, first=True, to_dict=False)
        resource = resource or abort(403, "Resource <{0}> is not in ACL".format(resource_name))

        parent_ids = RoleRelationCRUD.recursive_parent_ids(rid)
        group_ids = cls.get_group_ids(resource.id)

        perms = []
        for parent_id in parent_ids:
            id2perms = RoleRelationCache.get_resources(parent_id)
            perms += id2perms['id2perms'].get(parent_id, [])

            for group_id in group_ids:
                perms += id2perms['group2perms'].get(group_id, [])

        return set(perms)
