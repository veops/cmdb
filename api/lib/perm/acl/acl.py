# -*- coding:utf-8 -*-

import functools

import six
from flask import current_app, g, request
from flask import session, abort

from api.lib.perm.acl.cache import AppCache
from api.models.acl import ResourceType
from api.models.acl import Resource
from api.lib.perm.acl.resource import ResourceCRUD


class ACLManager(object):
    def __init__(self):
        self.user_info = session["acl"] if "acl" in session else {}
        self.app_id = AppCache.get('cmdb')
        if not self.app_id:
            raise Exception("cmdb not in acl apps")
        self.app_id = self.app_id.id

    def add_resource(self, name, resource_type_name=None):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        if resource_type:
            return abort(400, "ResourceType <{0}> cannot be found".format(resource_type_name))

        ResourceCRUD.add(name, resource_type.id, self.app_id)

    def grant_resource_to_role(self, name, role, resource_type_name=None):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        if resource_type:
            return abort(400, "ResourceType <{0}> cannot be found".format(resource_type_name))

    def del_resource(self, name, resource_type_name=None):
        resource_type = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        if resource_type:
            return abort(400, "ResourceType <{0}> cannot be found".format(resource_type_name))

        resource = Resource.get_by(resource_type_id=resource_type.id,
                                   app_id=self.app_id,
                                   name=name,
                                   first=True,
                                   to_dict=False)
        if resource:
            ResourceCRUD.delete(resource.id)

    def get_resources(self, resource_type_name=None):
        if "acl" not in session:
            abort(405)
        return []

    def has_permission(self, resource_name, resource_type, perm):
        if "acl" not in session:
            abort(405)
        return True


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


def can_access_resources(resource_type):
    def decorator_can_access_resources(func):
        @functools.wraps(func)
        def wrapper_can_access_resources(*args, **kwargs):
            if current_app.config.get("USE_ACL"):
                res = ACLManager().get_resources(resource_type)
                result = {i.get("name"): i.get("permissions") for i in res}
                if hasattr(g, "resources"):
                    g.resources.update({resource_type: result})
                else:
                    g.resources = {resource_type: result}
            return func(*args, **kwargs)

        return wrapper_can_access_resources

    return decorator_can_access_resources


def has_perm(resources, resource_type, perm):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not resources:
                return

            if current_app.config.get("USE_ACL"):
                validate_permission(resources, resource_type, perm)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm


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
