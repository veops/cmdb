import functools

from flask import abort, session
from api.lib.common_setting.acl import ACLManager
from api.lib.common_setting.resp_format import ErrFormat
from api.lib.perm.acl.acl import is_app_admin


def perms_role_required(app_name, resource_type_name, resource_name, perm, role_name=None):
    def decorator_perms_role_required(func):
        @functools.wraps(func)
        def wrapper_required(*args, **kwargs):
            acl = ACLManager(app_name)
            has_perms = False
            try:
                has_perms = acl.role_has_perms(session["acl"]['rid'], resource_name, resource_type_name, perm)
            except Exception as e:
                # resource_type not exist, continue check role
                if role_name:
                    if role_name not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin(app_name):
                        abort(403, ErrFormat.role_required.format(role_name))

                    return func(*args, **kwargs)
                else:
                    abort(403, ErrFormat.resource_no_permission.format(resource_name, perm))

            if not has_perms:
                if role_name:
                    if role_name not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin(app_name):
                        abort(403, ErrFormat.role_required.format(role_name))
                else:
                    abort(403, ErrFormat.resource_no_permission.format(resource_name, perm))

            return func(*args, **kwargs)

        return wrapper_required

    return decorator_perms_role_required
