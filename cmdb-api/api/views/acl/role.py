# -*- coding:utf-8 -*-

from flask import abort
from flask import current_app
from flask import g
from flask import request

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl import validate_app
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.role import RoleCRUD
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.auth import auth_only_for_acl
from api.lib.perm.auth import auth_with_app_token
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class RoleView(APIView):
    url_prefix = ("/roles", "/roles/<int:rid>")

    @validate_app
    @auth_with_app_token
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')
        is_all = request.values.get('is_all', True)
        is_all = True if is_all in current_app.config.get("BOOL_TRUE") else False
        user_role = request.values.get('user_role', True)
        user_only = request.values.get('user_only', False)
        user_role = True if user_role in current_app.config.get("BOOL_TRUE") else False
        user_only = True if user_only in current_app.config.get("BOOL_TRUE") else False

        numfound, roles = RoleCRUD.search(q, app_id, page, page_size, user_role, is_all, user_only)

        id2parents = RoleRelationCRUD.get_parents([i.id for i in roles], app_id=app_id)

        roles = [i.to_dict() for i in roles]
        for i in roles:
            i.pop('password', None)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            id2parents=id2parents,
                            roles=roles)

    @args_required('name')
    @validate_app
    @auth_with_app_token
    @args_validate(RoleCRUD.cls, exclude_args=['app_id'])
    def post(self):
        name = request.values.get('name')
        app_id = request.values.get('app_id')
        password = request.values.get('password')
        _is_app_admin = request.values.get('is_app_admin', False)

        role = RoleCRUD.add_role(name, app_id, password=password, is_app_admin=_is_app_admin)

        return self.jsonify(role.to_dict())

    @auth_only_for_acl
    @args_validate(RoleCRUD.cls, exclude_args=['app_id'])
    def put(self, rid):
        role = RoleCRUD.update_role(rid, **request.values)

        return self.jsonify(role.to_dict())

    @auth_only_for_acl
    def delete(self, rid):
        RoleCRUD.delete_role(rid)

        return self.jsonify(rid=rid)


class RoleRelationView(APIView):
    url_prefix = ("/roles/<int:rid>/parents", "/roles/<int:rid>/users", "/roles/<int:rid>/children")

    @auth_with_app_token
    @validate_app
    def get(self, rid):
        app_id = request.values.get('app_id')
        app = AppCache.get(app_id)
        if app and app.name == "acl":
            app_id = None  # global

        users = RoleRelationCRUD.get_users_by_rid(rid, app_id)

        return self.jsonify(users=users)

    @auth_only_for_acl
    @validate_app
    @args_validate(RoleRelationCRUD.cls, exclude_args=['app_id'])
    def post(self, rid):

        app_id = request.values.get('app_id')
        app = AppCache.get(app_id)
        if app and app.name == "acl":
            app_id = None  # global

        role = RoleCache.get(rid) or abort(400, ErrFormat.role_not_found.format("id={}".format(rid)))

        if request.values.get('parent_id'):
            parent_id = request.values.get('parent_id')

            res = RoleRelationCRUD.add(role, parent_id, [rid], app_id)

            return self.jsonify(res)
        elif request.values.get("child_ids") and isinstance(request.values['child_ids'], list):
            res = RoleRelationCRUD.add(role, rid, request.values['child_ids'], app_id)

            return self.jsonify(res)

        else:
            return abort(400, ErrFormat.invalid_request)

    @args_required('parent_id')
    @auth_only_for_acl
    @validate_app
    def delete(self, rid):
        parent_id = request.values.get('parent_id')

        app_id = request.values.get('app_id')
        app = AppCache.get(app_id)
        if app and app.name == "acl":
            app_id = None  # global

        RoleRelationCRUD.delete2(parent_id, rid, app_id)

        return self.jsonify(parent_id=parent_id, child_id=rid)


class RoleResourcesView(APIView):
    url_prefix = "/roles/<int:rid>/resources"

    @auth_with_app_token
    @validate_app
    def get(self, rid):
        resource_type_id = request.values.get('resource_type_id')
        group_flat = request.values.get('group_flat', True)
        res = RoleCRUD.recursive_resources(rid, request.values['app_id'], resource_type_id, group_flat, to_record=True)

        return self.jsonify(res)


class RoleHasPermissionView(APIView):
    url_prefix = "/roles/has_perm"

    @args_required('resource_name')
    @args_required('resource_type_name')
    @args_required('perm')
    @validate_app
    @auth_with_app_token
    def get(self):
        if not request.values.get('rid'):
            role = RoleCache.get_by_name(None, g.user.username)
            role or abort(404, ErrFormat.role_not_found.format(g.user.username))
        else:
            role = RoleCache.get(int(request.values.get('rid')))

        app_id = request.values.get('app_id')
        if is_app_admin(app_id):
            return self.jsonify(result=True)

        resource_name = request.values.get('resource_name')
        resource_type_name = request.values.get('resource_type_name')
        perm = request.values.get('perm')
        result = RoleCRUD.has_permission(role.id, resource_name, resource_type_name, app_id, perm)

        return self.jsonify(result=result)
