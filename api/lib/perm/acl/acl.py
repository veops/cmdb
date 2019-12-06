# -*- coding:utf-8 -*-

import functools

import six
from flask import current_app, g, request
from flask import session, abort

from api.lib.cmdb.const import ResourceTypeEnum as CmdbResourceType
from api.lib.cmdb.const import RoleEnum
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.permission import PermissionCRUD
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.role import RoleCRUD
from api.models.acl import Resource
from api.models.acl import ResourceGroup
from api.models.acl import ResourceType
from api.models.acl import Role

CMDB_RESOURCE_TYPES = CmdbResourceType.all()


class ACLManager(object):
    def __init__(self):
        self.app_id = AppCache.get('cmdb')
        if not self.app_id:
            raise Exception("cmdb not in acl apps")
        self.app_id = self.app_id.id

    def _get_resource(self, name, resource_type_name):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        resource_type or abort(404, "ResourceType <{0}> cannot be found".format(resource_type_name))

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

        return Role.get_by(name=name, app_id=self.app_id, first=True, to_dict=False)

    def add_resource(self, name, resource_type_name=None):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        resource_type or abort(404, "ResourceType <{0}> cannot be found".format(resource_type_name))

        ResourceCRUD.add(name, resource_type.id, self.app_id)

    def grant_resource_to_role(self, name, role, resource_type_name=None, permissions=None):
        resource = self._get_resource(name, resource_type_name)

        role = self._get_role(role)

        if resource:
            PermissionCRUD.grant(role.id, permissions, resource_id=resource.id)
        else:
            group = self._get_resource_group(name)
            if group:
                PermissionCRUD.grant(role.id, permissions, group_id=group.id)

    def del_resource(self, name, resource_type_name=None):
        resource = self._get_resource(name, resource_type_name)
        if resource:
            ResourceCRUD.delete(resource.id)

    def has_permission(self, resource_name, resource_type, perm):

        role = self._get_role(g.user.username)

        role or abort(404, "Role <{0}> is not found".format(g.user.username))

        return RoleCRUD.has_permission(role.id, resource_name, resource_type, self.app_id, perm)


def validate_permission(resources, resource_type, perm):
    if not resources:
        return

    if current_app.config.get("USE_ACL"):
        if g.user.username == "worker":
            return

        resources = [resources] if isinstance(resources, six.string_types) else resources
        for resource in resources:
            if not ACLManager().has_permission(resource, resource_type, perm):
                return abort(403, "has no permission")


def has_perm(resources, resource_type, perm):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not resources:
                return

            if current_app.config.get("USE_ACL"):
                if is_app_admin():
                    return func(*args, **kwargs)

                validate_permission(resources, resource_type, perm)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm


def is_app_admin():
    if RoleEnum.CONFIG in session.get("acl", {}).get("parentRoles", []):
        return True

    return False


def has_perm_from_args(arg_name, resource_type, perm, callback=None):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not arg_name:
                return
            resource = request.view_args.get(arg_name) or request.values.get(arg_name)
            if callback is not None and resource:
                resource = callback(resource)

            if current_app.config.get("USE_ACL") and resource:
                if is_app_admin():
                    return func(*args, **kwargs)

                validate_permission(resource, resource_type, perm)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm


def role_required(role_name):
    def decorator_role_required(func):
        @functools.wraps(func)
        def wrapper_role_required(*args, **kwargs):
            if not role_name:
                return

            if current_app.config.get("USE_ACL"):
                if role_name not in session.get("acl", {}).get("parentRoles", []):
                    return abort(403, "Role {0} is required".format(role_name))
            return func(*args, **kwargs)

        return wrapper_role_required

    return decorator_role_required
