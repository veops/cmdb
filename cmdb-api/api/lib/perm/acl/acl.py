# -*- coding:utf-8 -*-

import functools
import hashlib

import requests
import six
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import current_user

from api.extensions import cache
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.permission import PermissionCRUD
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.role import RoleCRUD
from api.lib.perm.acl.role import RoleRelationCRUD
from api.models.acl import App
from api.models.acl import Resource
from api.models.acl import ResourceGroup
from api.models.acl import ResourceType
from api.models.acl import Role


def get_access_token():
    url = "{0}/acl/apps/token".format(current_app.config.get('ACL_URI'))
    payload = dict(app_id=current_app.config.get('APP_ID'),
                   secret_key=hashlib.md5(current_app.config.get('APP_SECRET_KEY').encode('utf-8')).hexdigest())
    try:
        res = requests.post(url, data=payload).json()
        return res.get("token")
    except Exception as e:
        current_app.logger.error(str(e))


class AccessTokenCache(object):
    TOKEN_KEY = 'TICKET::AccessToken'

    @classmethod
    def get(cls):
        if cache.get(cls.TOKEN_KEY) is not None and cache.get(cls.TOKEN_KEY) != "":
            return cache.get(cls.TOKEN_KEY)

        res = get_access_token() or ""

        cache.set(cls.TOKEN_KEY, res, timeout=60 * 60)
        return res

    @classmethod
    def clean(cls):
        cache.clear(cls.TOKEN_KEY)


class ACLManager(object):
    def __init__(self, app=None):
        self.app = AppCache.get(app or 'cmdb')
        if not self.app:
            raise Exception(ErrFormat.app_not_found.format(app))
        self.app_id = self.app.id

    def _get_resource(self, name, resource_type_name):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        resource_type or abort(404, ErrFormat.resource_type_not_found.format(resource_type_name))

        return Resource.get_by(resource_type_id=resource_type.id,
                               app_id=self.app_id,
                               name=name,
                               first=True,
                               to_dict=False)

    def _get_resource_group(self, name):
        return ResourceGroup.get_by(
            app_id=self.app_id,
            name=name,
            first=True,
            to_dict=False
        )

    def _get_role(self, name):
        user = UserCache.get(name)
        if user:
            return Role.get_by(name=name, uid=user.uid, first=True, to_dict=False)

        return (Role.get_by(name=name, app_id=self.app_id, first=True, to_dict=False) or
                Role.get_by(name=name, first=True, to_dict=False))

    def add_resource(self, name, resource_type_name=None):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        resource_type or abort(404, ErrFormat.resource_type_not_found.format(resource_type_name))

        uid = AuditCRUD.get_current_operate_uid()
        ResourceCRUD.add(name, resource_type.id, self.app_id, uid)

    def update_resource(self, name, new_name, resource_type_name=None):
        resource = self._get_resource(name, resource_type_name)

        if resource is None:
            self.add_resource(new_name, resource_type_name)
        else:
            ResourceCRUD.update(resource.id, new_name)

    def grant_resource_to_role(self, name, role, resource_type_name=None, permissions=None):
        resource = self._get_resource(name, resource_type_name)

        role = self._get_role(role)

        if resource:
            PermissionCRUD.grant(role.id, permissions, resource_id=resource.id)
        else:
            group = self._get_resource_group(name)
            if group:
                PermissionCRUD.grant(role.id, permissions, group_id=group.id)

    def grant_resource_to_role_by_rid(self, name, rid, resource_type_name=None, permissions=None, rebuild=True):
        resource = self._get_resource(name, resource_type_name)

        if resource:
            PermissionCRUD.grant(rid, permissions, resource_id=resource.id, rebuild=rebuild)
        else:
            group = self._get_resource_group(name)
            if group:
                PermissionCRUD.grant(rid, permissions, group_id=group.id, rebuild=rebuild)

    def revoke_resource_from_role(self, name, role, resource_type_name=None, permissions=None):
        resource = self._get_resource(name, resource_type_name)
        role = self._get_role(role)

        if resource:
            PermissionCRUD.revoke(role.id, permissions, resource_id=resource.id)
        else:
            group = self._get_resource_group(name)
            if group:
                PermissionCRUD.revoke(role.id, permissions, group_id=group.id)

    def revoke_resource_from_role_by_rid(self, name, rid, resource_type_name=None, permissions=None, rebuild=True):
        resource = self._get_resource(name, resource_type_name)

        if resource:
            PermissionCRUD.revoke(rid, permissions, resource_id=resource.id, rebuild=rebuild)
        else:
            group = self._get_resource_group(name)
            if group:
                PermissionCRUD.revoke(rid, permissions, group_id=group.id, rebuild=rebuild)

    def del_resource(self, name, resource_type_name=None, rebuild=True):
        resource = self._get_resource(name, resource_type_name)
        if resource:
            return ResourceCRUD.delete(resource.id, rebuild=rebuild)

    def has_permission(self, resource_name, resource_type, perm, resource_id=None):
        if is_app_admin(self.app_id):
            return True

        role = self._get_role(current_user.username)

        role or abort(404, ErrFormat.role_not_found.format(current_user.username))

        return RoleCRUD.has_permission(role.id, resource_name, resource_type, self.app_id, perm,
                                       resource_id=resource_id)

    @staticmethod
    def get_user_info(username, app_id=None):
        user = UserCache.get(username)
        if not user:
            user = RoleCache.get_by_name(app_id, username) or RoleCache.get_by_name(None, username)  # FIXME

        if not user:
            return abort(404, ErrFormat.user_not_found.format(username))
        user = user.to_dict()

        role = Role.get_by(uid=user['uid'], first=True, to_dict=False) if user.get('uid') else None
        if role is not None:
            user["rid"] = role.id
            if app_id is None:
                parent_ids = []
                apps = App.get_by(to_dict=False)
                for app in apps:
                    parent_ids.extend(RoleRelationCRUD.recursive_parent_ids(role.id, app.id))
            else:
                parent_ids = RoleRelationCRUD.recursive_parent_ids(role.id, app_id)

            user['parents'] = [RoleCache.get(rid).name for rid in set(parent_ids) if RoleCache.get(rid)]
        else:
            user['parents'] = []
            user['rid'] = user['id'] if user.get('id') else None
            if user['rid']:
                parent_ids = RoleRelationCRUD.recursive_parent_ids(user['rid'], app_id)
                user['parents'] = [RoleCache.get(rid).name for rid in set(parent_ids) if RoleCache.get(rid)]

        return user

    def get_resources(self, resource_type_name=None):
        role = self._get_role(current_user.username)

        role or abort(404, ErrFormat.role_not_found.format(current_user.username))
        rid = role.id

        return RoleCRUD.recursive_resources(rid, self.app_id, resource_type_name).get('resources')

    @staticmethod
    def authenticate_with_token(token):
        url = "{0}/acl/auth_with_token".format(current_app.config.get('ACL_URI'))
        try:
            return requests.post(url, json={"token": token},
                                 headers={'App-Access-Token': AccessTokenCache.get()}).json()
        except:
            return {}


def validate_permission(resources, resource_type, perm, app=None):
    if not resources:
        return

    if current_app.config.get("USE_ACL"):
        if current_user.username == "worker":
            return

        resources = [resources] if isinstance(resources, six.string_types) else resources
        for resource in resources:
            if not ACLManager(app).has_permission(resource, resource_type, perm):
                return abort(403, ErrFormat.resource_no_permission.format(resource, perm))


def has_perm(resources, resource_type, perm, app=None):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not resources:
                return

            if current_app.config.get("USE_ACL"):
                if is_app_admin(app):
                    return func(*args, **kwargs)

                validate_permission(resources, resource_type, perm, app)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm


def is_app_admin(app=None):
    app = app or 'cmdb'
    app = AppCache.get(app)
    if app is None:
        return False

    app_id = app.id
    if 'acl_admin' in session.get("acl", {}).get("parentRoles", []):
        return True

    for role_name in session.get("acl", {}).get("parentRoles", []):
        role = RoleCache.get_by_name(app_id, role_name)
        if role and role.is_app_admin:
            return True

    return False


def is_admin():
    if 'acl_admin' in session.get("acl", {}).get("parentRoles", []):
        return True

    return False


def admin_required(app=None):
    def decorator_admin_required(func):
        @functools.wraps(func)
        def wrapper_admin_required(*args, **kwargs):
            if is_app_admin(app):
                return func(*args, **kwargs)
            return abort(403, ErrFormat.admin_required)

        return wrapper_admin_required

    return decorator_admin_required


def has_perm_from_args(arg_name, resource_type, perm, callback=None, app=None):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not arg_name:
                return
            resource = request.view_args.get(arg_name) or request.values.get(arg_name)
            if callback is not None and resource:
                resource = callback(resource)

            if current_app.config.get("USE_ACL") and resource:
                if is_app_admin(app):
                    return func(*args, **kwargs)

                validate_permission(resource, resource_type, perm, app)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm


def role_required(role_name, app=None):
    def decorator_role_required(func):
        @functools.wraps(func)
        def wrapper_role_required(*args, **kwargs):
            if not role_name:
                return

            if current_app.config.get("USE_ACL"):
                if getattr(current_user, 'username', None) == "worker":
                    return func(*args, **kwargs)

                if role_name not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin(app):
                    return abort(403, ErrFormat.role_required.format(role_name))
            return func(*args, **kwargs)

        return wrapper_role_required

    return decorator_role_required
