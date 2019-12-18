# -*- coding:utf-8 -*-

from api.extensions import cache
from api.extensions import db
from api.models.acl import App
from api.models.acl import Permission
from api.models.acl import Role
from api.models.acl import User


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

    @classmethod
    def get(cls, key):
        user = cache.get(cls.PREFIX_ID.format(key)) or \
               cache.get(cls.PREFIX_NAME.format(key)) or \
               cache.get(cls.PREFIX_NICK.format(key))
        if not user:
            user = User.query.get(key) or \
                   User.query.get_by_username(key) or \
                   User.query.get_by_nickname(key)
        if user:
            cls.set(user)

        return user

    @classmethod
    def set(cls, user):
        cache.set(cls.PREFIX_ID.format(user.uid), user)
        cache.set(cls.PREFIX_NAME.format(user.username), user)
        cache.set(cls.PREFIX_NICK.format(user.nickname), user)

    @classmethod
    def clean(cls, user):
        cache.delete(cls.PREFIX_ID.format(user.uid))
        cache.delete(cls.PREFIX_NAME.format(user.username))
        cache.delete(cls.PREFIX_NICK.format(user.nickname))


class RoleCache(object):
    PREFIX_ID = "Role::id::{0}"
    PREFIX_NAME = "Role::app_id::{0}::name::{1}"

    @classmethod
    def get_by_name(cls, app_id, name):
        role = cache.get(cls.PREFIX_NAME.format(app_id, name))
        if role is None:
            role = Role.get_by(app_id=app_id, name=name, first=True, to_dict=False)
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


class RoleRelationCache(object):
    PREFIX_PARENT = "RoleRelationParent::id::{0}"
    PREFIX_CHILDREN = "RoleRelationChildren::id::{0}"
    PREFIX_RESOURCES = "RoleRelationResources::id::{0}"

    @classmethod
    def get_parent_ids(cls, rid):
        parent_ids = cache.get(cls.PREFIX_PARENT.format(rid))
        if not parent_ids:
            from api.lib.perm.acl.role import RoleRelationCRUD
            parent_ids = RoleRelationCRUD.get_parent_ids(rid)
            cache.set(cls.PREFIX_PARENT.format(rid), parent_ids, timeout=0)

        return parent_ids

    @classmethod
    def get_child_ids(cls, rid):
        child_ids = cache.get(cls.PREFIX_CHILDREN.format(rid))
        if not child_ids:
            from api.lib.perm.acl.role import RoleRelationCRUD
            child_ids = RoleRelationCRUD.get_child_ids(rid)
            cache.set(cls.PREFIX_CHILDREN.format(rid), child_ids, timeout=0)

        return child_ids

    @classmethod
    def get_resources(cls, rid):
        """
        :param rid: 
        :return: {id2perms: {resource_id: [perm,]}, group2perms: {group_id: [perm, ]}}
        """
        resources = cache.get(cls.PREFIX_RESOURCES.format(rid))
        if not resources:
            from api.lib.perm.acl.role import RoleCRUD
            resources = RoleCRUD.get_resources(rid)
            cache.set(cls.PREFIX_RESOURCES.format(rid), resources, timeout=0)

        return resources or {}

    @classmethod
    def rebuild(cls, rid):
        cls.clean(rid)
        db.session.close()
        cls.get_parent_ids(rid)
        cls.get_child_ids(rid)
        cls.get_resources(rid)

    @classmethod
    def clean(cls, rid):
        cache.delete(cls.PREFIX_PARENT.format(rid))
        cache.delete(cls.PREFIX_CHILDREN.format(rid))
        cache.delete(cls.PREFIX_RESOURCES.format(rid))


class PermissionCache(object):
    PREFIX_ID = "Permission::id::{0}"
    PREFIX_NAME = "Permission::name::{0}"

    @classmethod
    def get(cls, key):
        perm = cache.get(cls.PREFIX_ID.format(key))
        perm = perm or cache.get(cls.PREFIX_NAME.format(key))
        if perm is None:
            perm = Permission.get_by_id(key)
            perm = perm or Permission.get_by(name=key, first=True, to_dict=False)
            if perm is not None:
                cache.set(cls.PREFIX_ID.format(key), perm)

        return perm

    @classmethod
    def clean(cls, key):
        cache.delete(cls.PREFIX_ID.format(key))
        cache.delete(cls.PREFIX_NAME.format(key))
