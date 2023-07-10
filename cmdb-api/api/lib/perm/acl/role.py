# -*- coding:utf-8 -*-


import time

import six
from flask import abort
from flask import current_app

from api.extensions import db
from api.lib.perm.acl.app import AppCRUD
from api.lib.perm.acl.audit import AuditCRUD, AuditOperateType, AuditScope
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import HasResourceRoleCache
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import RoleRelationCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.const import OperateType
from api.lib.perm.acl.resource import ResourceGroupCRUD
from api.lib.perm.acl.resp_format import ErrFormat
from api.models.acl import Resource, ResourceGroup
from api.models.acl import ResourceGroupItems
from api.models.acl import ResourceType
from api.models.acl import Role
from api.models.acl import RolePermission
from api.models.acl import RoleRelation
from api.tasks.acl import op_record
from api.tasks.acl import role_rebuild


class RoleRelationCRUD(object):
    cls = RoleRelation

    @staticmethod
    def get_parents(rids=None, uids=None, app_id=None, all_app=False):
        rid2uid = dict()
        if uids is not None:
            uids = [uids] if isinstance(uids, six.integer_types) else uids
            rids = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.in_(uids))
            rid2uid = {i.id: i.uid for i in rids}
            rids = [i.id for i in rids]
        else:
            rids = [rids] if isinstance(rids, six.integer_types) else rids

        if app_id is not None:
            res = db.session.query(RoleRelation).filter(
                RoleRelation.child_id.in_(rids)).filter(RoleRelation.app_id == app_id).filter(
                RoleRelation.deleted.is_(False)).union(
                db.session.query(RoleRelation).filter(
                    RoleRelation.child_id.in_(rids)).filter(RoleRelation.app_id.is_(None)).filter(
                    RoleRelation.deleted.is_(False)))

        elif not all_app:
            res = db.session.query(RoleRelation).filter(
                RoleRelation.child_id.in_(rids)).filter(RoleRelation.app_id.is_(None)).filter(
                RoleRelation.deleted.is_(False))
        else:
            res = db.session.query(RoleRelation).filter(
                RoleRelation.child_id.in_(rids)).filter(RoleRelation.deleted.is_(False))

        id2parents = {}
        for i in res:
            id2parents.setdefault(rid2uid.get(i.child_id, i.child_id), []).append(RoleCache.get(i.parent_id).to_dict())

        return id2parents

    @staticmethod
    def get_parent_ids(rid, app_id):
        if app_id is not None:
            return [i.parent_id for i in RoleRelation.get_by(child_id=rid, app_id=app_id, to_dict=False)] + \
                   [i.parent_id for i in RoleRelation.get_by(child_id=rid, app_id=None, to_dict=False)]
        else:
            return [i.parent_id for i in RoleRelation.get_by(child_id=rid, app_id=app_id, to_dict=False)]

    @staticmethod
    def get_child_ids(rid, app_id):
        if app_id is not None:
            return [i.child_id for i in RoleRelation.get_by(parent_id=rid, app_id=app_id, to_dict=False)] + \
                   [i.child_id for i in RoleRelation.get_by(parent_id=rid, app_id=None, to_dict=False)]
        else:
            return [i.child_id for i in RoleRelation.get_by(parent_id=rid, app_id=app_id, to_dict=False)]

    @classmethod
    def recursive_parent_ids(cls, rid, app_id):
        all_parent_ids = set()

        def _get_parent(_id):
            all_parent_ids.add(_id)
            parent_ids = RoleRelationCache.get_parent_ids(_id, app_id)
            for parent_id in parent_ids:
                _get_parent(parent_id)

        _get_parent(rid)

        return all_parent_ids

    @classmethod
    def recursive_child_ids(cls, rid, app_id):
        all_child_ids = set()

        def _get_children(_id):
            all_child_ids.add(_id)
            child_ids = RoleRelationCache.get_child_ids(_id, app_id)
            for child_id in child_ids:
                _get_children(child_id)

        _get_children(rid)

        return all_child_ids

    @classmethod
    def get_users_by_rid(cls, rid, app_id, rid2obj=None, uid2obj=None):
        rid2obj = rid2obj or dict()
        uid2obj = uid2obj or dict()

        users = []
        rids = cls.recursive_child_ids(rid, app_id)
        for rid in rids:
            if rid not in rid2obj:
                rid2obj[rid] = RoleCache.get(rid)

            role = rid2obj[rid]
            if role and role.uid:
                if role.uid and role.uid not in uid2obj:
                    uid2obj[role.uid] = UserCache.get(role.uid)

                u = uid2obj.get(role.uid)
                u = u and u.to_dict()
                if u:
                    u.update(dict(role=role.to_dict()))
                    users.append(u)

        # todo role read log
        # user_id = AuditCRUD.get_current_operate_uid()
        # audit_role_log.apply_async(args=(app_id, user_id, result.copy()),
        #                            queue=ACL_QUEUE)

        return users

    @classmethod
    def add(cls, role, parent_id, child_ids, app_id):
        result = []
        for child_id in child_ids:
            existed = RoleRelation.get_by(parent_id=parent_id, child_id=child_id, app_id=app_id)
            if existed:
                continue

            RoleRelationCache.clean(parent_id, app_id)
            RoleRelationCache.clean(child_id, app_id)

            if parent_id in cls.recursive_child_ids(child_id, app_id):
                return abort(400, ErrFormat.inheritance_dead_loop)

            if app_id is None:
                for app in AppCRUD.get_all():
                    if app.name != "acl":
                        RoleRelationCache.clean(child_id, app.id)

            result.append(RoleRelation.create(parent_id=parent_id, child_id=child_id, app_id=app_id).to_dict())

        AuditCRUD.add_role_log(app_id, AuditOperateType.role_relation_add,
                               AuditScope.role_relation, role.id, {}, {},
                               {'child_ids': list(child_ids), 'parent_ids': [parent_id], }
                               )
        return result

    @classmethod
    def delete(cls, _id, app_id):
        existed = RoleRelation.get_by_id(_id) or abort(
            400, ErrFormat.role_relation_not_found.format("id={}".format(_id)))

        child_ids = cls.recursive_child_ids(existed.child_id, app_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id, app_id), queue=ACL_QUEUE)
        role = RoleCache.get(existed.parent_id)

        existed.soft_delete()

        RoleRelationCache.clean(existed.parent_id, app_id)
        RoleRelationCache.clean(existed.child_id, app_id)

        AuditCRUD.add_role_log(app_id, AuditOperateType.role_relation_delete,
                               AuditScope.role_relation, role.id, {}, {},
                               {'child_ids': list(child_ids), 'parent_ids': [existed.parent_id], }
                               )

    @classmethod
    def delete2(cls, parent_id, child_id, app_id):
        existed = RoleRelation.get_by(parent_id=parent_id, child_id=child_id, app_id=app_id, first=True, to_dict=False)
        existed or abort(400, ErrFormat.role_relation_not_found.format("{} -> {}".format(parent_id, child_id)))

        role = RoleCache.get(existed.parent_id)

        existed.soft_delete()

        child_ids = cls.recursive_child_ids(existed.child_id, app_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id, app_id), queue=ACL_QUEUE)

        RoleRelationCache.clean(existed.parent_id, app_id)
        RoleRelationCache.clean(existed.child_id, app_id)

        AuditCRUD.add_role_log(app_id, AuditOperateType.role_relation_delete,
                               AuditScope.role_relation, role.id, {}, {},
                               {'child_ids': list(child_ids), 'parent_ids': [existed.parent_id], }
                               )


class RoleCRUD(object):
    cls = Role

    @staticmethod
    def search(q, app_id, page=1, page_size=None, user_role=True, is_all=False, user_only=False):
        query = db.session.query(Role).filter(Role.deleted.is_(False))
        query1 = query.filter(Role.app_id == app_id).filter(Role.uid.is_(None))
        query2 = query.filter(Role.app_id.is_(None)).filter(Role.uid.is_(None))
        query = query1.union(query2)

        if user_role:
            query1 = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.isnot(None))
            query = query.union(query1)

        if user_only:
            query = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.isnot(None))

        if not is_all:
            role_ids = list(HasResourceRoleCache.get(app_id).keys())
            query = query.filter(Role.id.in_(role_ids))

        if q:
            query = query.filter(Role.name.ilike('%{0}%'.format(q)))

        numfound = query.count()

        return numfound, query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def add_role(name, app_id=None, is_app_admin=False, uid=None, password=None):
        if app_id and AppCache.get(app_id).name == "acl":
            app_id = None

        Role.get_by(name=name, app_id=app_id) and abort(400, ErrFormat.role_exists.format(name))

        if app_id is not None:
            Role.get_by(name=name, app_id=None) and abort(400, ErrFormat.global_role_exists.format(name))

        from api.lib.perm.acl.user import UserCRUD
        key, secret = UserCRUD.gen_key_secret()

        role = Role.create(name=name,
                           app_id=app_id,
                           is_app_admin=is_app_admin,
                           password=password,
                           key=key,
                           secret=secret,
                           uid=uid)

        AuditCRUD.add_role_log(app_id, AuditOperateType.create,
                               AuditScope.role, role.id, {}, role.to_dict(), {})

        return role

    @staticmethod
    def update_role(rid, **kwargs):
        kwargs.pop('app_id', None)

        role = Role.get_by_id(rid) or abort(404, ErrFormat.role_not_found.format("rid={}".format(rid)))

        origin = role.to_dict()

        RoleCache.clean(rid)

        role = role.update(**kwargs)
        AuditCRUD.add_role_log(role.app_id, AuditOperateType.update,
                               AuditScope.role, role.id, origin, role.to_dict(), {},
                               )

        return role

    @staticmethod
    def get_by_name(name, app_id):

        role = Role.get_by(name=name, app_id=app_id)

        return role

    @classmethod
    def delete_role(cls, rid):
        from api.lib.perm.acl.acl import is_admin

        role = Role.get_by_id(rid) or abort(404, ErrFormat.role_not_found.format("rid={}".format(rid)))

        if not role.app_id and not is_admin():
            return abort(403, ErrFormat.admin_required)

        origin = role.to_dict()

        child_ids = []
        parent_ids = []
        recursive_child_ids = list(RoleRelationCRUD.recursive_child_ids(rid, role.app_id))

        for i in RoleRelation.get_by(parent_id=rid, to_dict=False):
            child_ids.append(i.child_id)
            i.soft_delete()

        for i in RoleRelation.get_by(child_id=rid, to_dict=False):
            parent_ids.append(i.parent_id)
            i.soft_delete()

        role_permissions = []
        for i in RolePermission.get_by(rid=rid, to_dict=False):
            role_permissions.append(i.to_dict())
            i.soft_delete()

        role.soft_delete()

        role_rebuild.apply_async(args=(recursive_child_ids, role.app_id), queue=ACL_QUEUE)

        RoleCache.clean(rid)
        RoleRelationCache.clean(rid, role.app_id)

        AuditCRUD.add_role_log(role.app_id, AuditOperateType.delete,
                               AuditScope.role, role.id, origin, {},
                               {'child_ids': child_ids, 'parent_ids': parent_ids,
                                'role_permissions': role_permissions, },
                               )

    @staticmethod
    def get_resources(rid, app_id):
        res = RolePermission.get_by(rid=rid, app_id=app_id, to_dict=False)
        id2perms = dict(id2perms={}, group2perms={})
        for i in res:
            if i.resource_id:
                id2perms['id2perms'].setdefault(i.resource_id, []).append(i.perm.name)
            elif i.group_id:
                id2perms['group2perms'].setdefault(i.group_id, []).append(i.perm.name)

        return id2perms

    @staticmethod
    def _extend_resources(rid, resource_type_id, app_id):
        res = RoleRelationCache.get_resources2(rid, app_id)
        resources = {_id: res['resources'][_id] for _id in res['resources']
                     if not resource_type_id or resource_type_id == res['resources'][_id]['resource_type_id']}
        groups = {_id: res['groups'][_id] for _id in res['groups']
                  if not resource_type_id or resource_type_id == res['groups'][_id]['resource_type_id']}

        return resources, groups

    @classmethod
    def recursive_resources(cls, rid, app_id, resource_type_id=None, group_flat=True, to_record=False):
        def _merge(a, b):
            for i in b:
                if i in a:
                    a[i]['permissions'] = list(set(a[i]['permissions'] + b[i]['permissions']))
                else:
                    a[i] = b[i]

            return a

        try:
            resource_type_id = resource_type_id and int(resource_type_id)
        except ValueError:
            resource_type = ResourceType.get_by(name=resource_type_id, app_id=app_id, first=True, to_dict=False)
            resource_type_id = resource_type and resource_type.id

        result = dict(resources=dict(), groups=dict())
        s = time.time()
        parent_ids = RoleRelationCRUD.recursive_parent_ids(rid, app_id)
        current_app.logger.info('parent ids {0}: {1}'.format(parent_ids, time.time() - s))
        for parent_id in parent_ids:

            _resources, _groups = cls._extend_resources(parent_id, resource_type_id, app_id)
            current_app.logger.info('middle1: {0}'.format(time.time() - s))
            _merge(result['resources'], _resources)
            current_app.logger.info('middle2: {0}'.format(time.time() - s))
            current_app.logger.info(len(_groups))
            if not group_flat:
                _merge(result['groups'], _groups)
            else:
                for rg_id in _groups:
                    items = ResourceGroupCRUD.get_items(rg_id)
                    for item in items:
                        if not resource_type_id or resource_type_id == item['resource_type_id']:
                            item.setdefault('permissions', [])
                            item['permissions'] = list(set(item['permissions'] + _groups[rg_id]['permissions']))
                            result['resources'][item['id']] = item
        current_app.logger.info('End: {0}'.format(time.time() - s))

        result['resources'] = list(result['resources'].values())
        result['groups'] = list(result['groups'].values())

        if to_record:
            op_record.apply_async(args=(app_id, rid, OperateType.READ, ["resources"]),
                                  queue=ACL_QUEUE)

            # todo role read log
            # user_id = AuditCRUD.get_current_operate_uid()
            # audit_role_log.apply_async(args=(app_id, user_id, result.copy()),
            #                            queue=ACL_QUEUE)
        return result

    @staticmethod
    def get_group_ids(resource_id):
        return [i.group_id for i in ResourceGroupItems.get_by(resource_id=resource_id, to_dict=False)]

    @classmethod
    def has_permission(cls, rid, resource_name, resource_type_name, app_id, perm, resource_id=None):
        current_app.logger.debug((rid, resource_name, resource_type_name, app_id, perm))
        if not resource_id:
            resource_type = ResourceType.get_by(app_id=app_id, name=resource_type_name, first=True, to_dict=False)
            resource_type or abort(404, ErrFormat.resource_type_not_found.format(resource_type_name))
            type_id = resource_type.id
            resource = Resource.get_by(name=resource_name, resource_type_id=type_id, first=True, to_dict=False)
            resource = resource or abort(403, ErrFormat.resource_not_found.format(resource_name))
            resource_id = resource.id

        parent_ids = RoleRelationCRUD.recursive_parent_ids(rid, app_id)
        group_ids = cls.get_group_ids(resource_id)
        for parent_id in parent_ids:
            id2perms = RoleRelationCache.get_resources(parent_id, app_id)
            current_app.logger.debug(id2perms)
            perms = id2perms['id2perms'].get(resource_id, [])
            if perms and {perm}.issubset(set(perms)):
                return True

            for group_id in group_ids:
                perms = id2perms['group2perms'].get(group_id, [])
                if perms and {perm}.issubset(set(perms)):
                    return True

        return False

    @classmethod
    def get_permissions(cls, rid, resource_name, app_id):

        resource = Resource.get_by(name=resource_name, first=True, to_dict=False)
        resource = resource or abort(403, ErrFormat.resource_not_found.format(resource_name))

        parent_ids = RoleRelationCRUD.recursive_parent_ids(rid, app_id)
        group_ids = cls.get_group_ids(resource.id)

        perms = []
        for parent_id in parent_ids:
            id2perms = RoleRelationCache.get_resources(parent_id, app_id)
            perms += id2perms['id2perms'].get(parent_id, [])

            for group_id in group_ids:
                perms += id2perms['group2perms'].get(group_id, [])

        return set(perms)

    @classmethod
    def list_resources(cls, app_id, rids, resource_type_id=None, q=None):

        query = db.session.query(Resource, RolePermission).filter(
            Resource.app_id == app_id,
            Resource.deleted.is_(False),
            RolePermission.deleted.is_(False),
            RolePermission.rid.in_(rids),
        ).join(
            RolePermission, Resource.id == RolePermission.resource_id
        )

        if resource_type_id:
            query = query.filter(Resource.resource_type_id == resource_type_id)

        if q:
            query = query.filter(Resource.resource_type_id == resource_type_id)

        return query.all()

    @classmethod
    def list_resource_groups(cls, app_id, rids, resource_type_id=None, q=None):

        query = db.session.query(ResourceGroup, RolePermission).filter(
            ResourceGroup.app_id == app_id,
            ResourceGroup.deleted.is_(False),
            RolePermission.deleted.is_(False),
            RolePermission.rid.in_(rids),
        ).join(
            RolePermission, ResourceGroup.id == RolePermission.group_id
        )

        if resource_type_id:
            query = query.filter(ResourceGroup.resource_type_id == resource_type_id)

        if q:
            query = query.filter(ResourceGroup.resource_type_id == resource_type_id)

        return query.all()
