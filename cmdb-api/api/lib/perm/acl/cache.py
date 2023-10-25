# -*- coding:utf-8 -*-


import msgpack

from api.extensions import cache
from api.lib.decorator import flush_db
from api.lib.utils import Lock
from api.models.acl import App
from api.models.acl import Permission
from api.models.acl import Resource
from api.models.acl import ResourceGroup
from api.models.acl import Role
from api.models.acl import User


class AppAccessTokenCache(object):
    PREFIX = "AppAccessTokenCache::token::{}"

    @classmethod
    def get_app_id(cls, token):
        app_id = cache.get(cls.PREFIX.format(token))
        return app_id

    @classmethod
    def set(cls, token, app, timeout=7200):
        cache.set(token, cls.PREFIX.format(app.app_id), timeout=timeout)


class AppCache(object):
    PREFIX_ID = "App::id::{0}"
    PREFIX_NAME = "App::name::{0}"

    @classmethod
    def get(cls, key):
        app = cache.get(cls.PREFIX_ID.format(key)) or cache.get(cls.PREFIX_NAME.format(key))
        if app is None:
            app = App.get_by_id(key) or App.get_by(name=key, to_dict=False, first=True)
        if app is not None:
            cls.set(app)

        return app

    @classmethod
    def set(cls, app):
        cache.set(cls.PREFIX_ID.format(app.id), app)
        cache.set(cls.PREFIX_NAME.format(app.name), app)

    @classmethod
    def clean(cls, app):
        cache.delete(cls.PREFIX_ID.format(app.id))
        cache.delete(cls.PREFIX_NAME.format(app.name))


class UserCache(object):
    PREFIX_ID = "User::uid::{0}"
    PREFIX_NAME = "User::username::{0}"
    PREFIX_NICK = "User::nickname::{0}"
    PREFIX_WXID = "User::wxid::{0}"

    @classmethod
    def get(cls, key):
        user = (cache.get(cls.PREFIX_ID.format(key)) or
                cache.get(cls.PREFIX_NAME.format(key)) or
                cache.get(cls.PREFIX_NICK.format(key)) or
                cache.get(cls.PREFIX_WXID.format(key)))
        if not user:
            user = (User.query.get(key) or
                    User.query.get_by_username(key) or
                    User.query.get_by_nickname(key) or
                    User.query.get_by_wxid(key))
        if user:
            cls.set(user)

        return user

    @classmethod
    def set(cls, user):
        cache.set(cls.PREFIX_ID.format(user.uid), user)
        cache.set(cls.PREFIX_NAME.format(user.username), user)
        cache.set(cls.PREFIX_NICK.format(user.nickname), user)
        if user.wx_id:
            cache.set(cls.PREFIX_WXID.format(user.wx_id), user)

    @classmethod
    def clean(cls, user):
        cache.delete(cls.PREFIX_ID.format(user.uid))
        cache.delete(cls.PREFIX_NAME.format(user.username))
        cache.delete(cls.PREFIX_NICK.format(user.nickname))
        if user.wx_id:
            cache.delete(cls.PREFIX_WXID.format(user.wx_id))


class RoleCache(object):
    PREFIX_ID = "Role::id::{0}"
    PREFIX_NAME = "Role::app_id::{0}::name::{1}"

    @classmethod
    def get_by_name(cls, app_id, name):
        role = cache.get(cls.PREFIX_NAME.format(app_id, name))
        if role is None:
            role = Role.get_by(app_id=app_id, name=name, first=True, to_dict=False)
            if role is None and app_id is None:  # try global role
                role = Role.get_by(name=name, first=True, to_dict=False)

            if role is not None:
                cache.set(cls.PREFIX_NAME.format(app_id, name), role)

        return role

    @classmethod
    def get(cls, rid):
        role = cache.get(cls.PREFIX_ID.format(rid))
        if role is None:
            role = Role.get_by_id(rid)
            if role is not None:
                cache.set(cls.PREFIX_ID.format(rid), role)

        return role

    @classmethod
    def clean(cls, rid):
        cache.delete(cls.PREFIX_ID.format(rid))

    @classmethod
    def clean_by_name(cls, app_id, name):
        cache.delete(cls.PREFIX_NAME.format(app_id, name))


class HasResourceRoleCache(object):
    PREFIX_KEY = "HasResourceRoleCache::AppId::{0}"

    @classmethod
    def get(cls, app_id):
        return cache.get(cls.PREFIX_KEY.format(app_id)) or {}

    @classmethod
    def add(cls, rid, app_id):
        with Lock('HasResourceRoleCache'):
            c = cls.get(app_id)
            c[rid] = 1
            cache.set(cls.PREFIX_KEY.format(app_id), c, timeout=0)

    @classmethod
    def remove(cls, rid, app_id):
        with Lock('HasResourceRoleCache'):
            c = cls.get(app_id)
            c.pop(rid, None)
            cache.set(cls.PREFIX_KEY.format(app_id), c, timeout=0)


class RoleRelationCache(object):
    PREFIX_PARENT = "RoleRelationParent::id::{0}::AppId::{1}"
    PREFIX_CHILDREN = "RoleRelationChildren::id::{0}::AppId::{1}"
    PREFIX_RESOURCES = "RoleRelationResources::id::{0}::AppId::{1}"
    PREFIX_RESOURCES2 = "RoleRelationResources2::id::{0}::AppId::{1}"

    @classmethod
    def get_parent_ids(cls, rid, app_id):
        parent_ids = cache.get(cls.PREFIX_PARENT.format(rid, app_id))
        if not parent_ids:
            from api.lib.perm.acl.role import RoleRelationCRUD
            parent_ids = RoleRelationCRUD.get_parent_ids(rid, app_id)
            cache.set(cls.PREFIX_PARENT.format(rid, app_id), parent_ids, timeout=0)

        return parent_ids

    @classmethod
    def get_child_ids(cls, rid, app_id):
        child_ids = cache.get(cls.PREFIX_CHILDREN.format(rid, app_id))
        if not child_ids:
            from api.lib.perm.acl.role import RoleRelationCRUD
            child_ids = RoleRelationCRUD.get_child_ids(rid, app_id)
            cache.set(cls.PREFIX_CHILDREN.format(rid, app_id), child_ids, timeout=0)

        return child_ids

    @classmethod
    def get_resources(cls, rid, app_id):
        """
        :param rid: 
        :param app_id: 
        :return: {id2perms: {resource_id: [perm,]}, group2perms: {group_id: [perm, ]}}
        """
        resources = cache.get(cls.PREFIX_RESOURCES.format(rid, app_id))
        if not resources:
            from api.lib.perm.acl.role import RoleCRUD
            resources = RoleCRUD.get_resources(rid, app_id)
            if resources['id2perms'] or resources['group2perms']:
                cache.set(cls.PREFIX_RESOURCES.format(rid, app_id), resources, timeout=0)

        return resources or {}

    @classmethod
    def get_resources2(cls, rid, app_id):
        r_g = cache.get(cls.PREFIX_RESOURCES2.format(rid, app_id))
        if not r_g:
            res = cls.get_resources(rid, app_id)
            id2perms = res['id2perms']
            group2perms = res['group2perms']

            resources, groups = dict(), dict()
            for _id in id2perms:
                resource = ResourceCache.get(_id)
                if not resource:
                    continue
                resource = resource.to_dict()
                resource.update(dict(permissions=id2perms[_id]))
                resources[_id] = resource

            for _id in group2perms:
                group = ResourceGroupCache.get(_id)
                if not group:
                    continue
                group = group.to_dict()
                group.update(dict(permissions=group2perms[_id]))
                groups[_id] = group
            r_g = msgpack.dumps(dict(resources=resources, groups=groups))
            cache.set(cls.PREFIX_RESOURCES2.format(rid, app_id), r_g, timeout=0)

        return msgpack.loads(r_g, raw=False)

    @classmethod
    @flush_db
    def rebuild(cls, rid, app_id):
        cls.clean(rid, app_id)

        cls.get_parent_ids(rid, app_id)
        cls.get_child_ids(rid, app_id)
        resources = cls.get_resources(rid, app_id)
        if resources.get('id2perms') or resources.get('group2perms'):
            HasResourceRoleCache.add(rid, app_id)
        else:
            HasResourceRoleCache.remove(rid, app_id)
        cls.get_resources2(rid, app_id)

    @classmethod
    @flush_db
    def rebuild2(cls, rid, app_id):
        cache.delete(cls.PREFIX_RESOURCES2.format(rid, app_id))
        cls.get_resources2(rid, app_id)

    @classmethod
    def clean(cls, rid, app_id):
        cache.delete(cls.PREFIX_PARENT.format(rid, app_id))
        cache.delete(cls.PREFIX_CHILDREN.format(rid, app_id))
        cache.delete(cls.PREFIX_RESOURCES.format(rid, app_id))
        cache.delete(cls.PREFIX_RESOURCES2.format(rid, app_id))


class PermissionCache(object):
    PREFIX_ID = "Permission::id::{0}::ResourceTypeId::{1}"
    PREFIX_NAME = "Permission::name::{0}::ResourceTypeId::{1}"

    @classmethod
    def get(cls, key, rt_id):
        perm = cache.get(cls.PREFIX_ID.format(key, rt_id))
        perm = perm or cache.get(cls.PREFIX_NAME.format(key, rt_id))
        if perm is None:
            perm = Permission.get_by_id(key)
            perm = perm or Permission.get_by(name=key, resource_type_id=rt_id, first=True, to_dict=False)
            if perm is not None:
                cache.set(cls.PREFIX_ID.format(perm.id, rt_id), perm)
                cache.set(cls.PREFIX_NAME.format(perm.name, rt_id), perm)

        return perm


class ResourceCache(object):
    PREFIX_ID = "Resource::id::{0}"
    PREFIX_NAME = "Resource::type_id::{0}::name::{1}"

    @classmethod
    def get(cls, key, type_id=None):
        resource = cache.get(cls.PREFIX_ID.format(key)) or cache.get(cls.PREFIX_NAME.format(type_id, key))
        if resource is None:
            resource = Resource.get_by_id(key) or Resource.get_by(name=key,
                                                                  resource_type_id=type_id,
                                                                  to_dict=False,
                                                                  first=True)
        if resource is not None:
            cls.set(resource)

        return resource

    @classmethod
    def set(cls, resource):
        cache.set(cls.PREFIX_ID.format(resource.id), resource)
        cache.set(cls.PREFIX_NAME.format(resource.resource_type_id, resource.name), resource)

    @classmethod
    def clean(cls, resource):
        cache.delete(cls.PREFIX_ID.format(resource.id))
        cache.delete(cls.PREFIX_NAME.format(resource.resource_type_id, resource.name))


class ResourceGroupCache(object):
    PREFIX_ID = "ResourceGroup::id::{0}"
    PREFIX_NAME = "ResourceGroup::type_id::{0}::name::{1}"

    @classmethod
    def get(cls, key, type_id=None):
        group = cache.get(cls.PREFIX_ID.format(key)) or cache.get(cls.PREFIX_NAME.format(type_id, key))
        if group is None:
            group = ResourceGroup.get_by_id(key) or ResourceGroup.get_by(name=key,
                                                                         resource_type_id=type_id,
                                                                         to_dict=False,
                                                                         first=True)
        if group is not None:
            cls.set(group)

        return group

    @classmethod
    def set(cls, group):
        cache.set(cls.PREFIX_ID.format(group.id), group)
        cache.set(cls.PREFIX_NAME.format(group.resource_type_id, group.name), group)

    @classmethod
    def clean(cls, group):
        cache.delete(cls.PREFIX_ID.format(group.id))
        cache.delete(cls.PREFIX_NAME.format(group.resource_type_id, group.name))
