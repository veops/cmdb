# -*- coding:utf-8 -*-


from flask import abort
from flask import current_app
from flask import request

from api.lib.decorator import args_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.permission import PermissionCRUD
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.auth import auth_only_for_acl
from api.lib.perm.auth import auth_with_app_token
from api.lib.utils import handle_arg_list
from api.resource import APIView


class ResourcePermissionView(APIView):
    url_prefix = ("/resources/<int:resource_id>/permissions", "/resource_groups/<int:group_id>/permissions")

    @auth_with_app_token
    def get(self, resource_id=None, group_id=None):
        need_users = request.values.get('need_users', 1) in current_app.config.get('BOOL_TRUE')
        return self.jsonify(PermissionCRUD.get_all(resource_id, group_id, need_users=need_users))


class ResourcePermission2View(APIView):
    url_prefix = "/resource/permissions"

    @args_required('resource_name')
    @args_required('resource_type_name')
    @auth_with_app_token
    def get(self):
        resource_name = request.values.get('resource_name')
        resource_type_name = request.values.get('resource_type_name')
        app_id = request.values.get('app_id')

        return self.jsonify(PermissionCRUD.get_all2(resource_name, resource_type_name, app_id))


class RolePermissionGrantView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/grant',
                  '/roles/<int:rid>/resource_groups/<int:group_id>/grant',
                  '/roles/<int:rid>/resources/batch/grant2',  # by names
                  )

    @auth_only_for_acl
    def post(self, rid, resource_id=None, group_id=None):
        perms = handle_arg_list(request.values.get("perms"))

        if "batch" in request.url:
            resource_ids = request.values.get('resource_ids')
            perm_map = request.values.get('perm_map')
            resource_names = request.values.get('resource_names')
            resource_type_id = request.values.get('resource_type_id')
            app = AppCache.get(request.values.get('app_id'))
            PermissionCRUD.batch_grant_by_resource_names(rid, perms, resource_type_id, resource_names,
                                                         resource_ids, perm_map, app_id=app and app.id)

            return self.jsonify(rid=rid, resource_names=resource_names, resource_type_id=resource_type_id, perms=perms)

        PermissionCRUD.grant(rid, perms, resource_id=resource_id, group_id=group_id)

        return self.jsonify(rid=rid, resource_id=resource_id, group_id=group_id, perms=perms)


class RolePermissionGrant2View(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/grant2',)

    def post(self, rid, resource_id):
        if not ACLManager(request.values.get('app_id')).has_permission(None, None, 'grant', resource_id):
            return abort(403, ErrFormat.no_permission2)

        perms = handle_arg_list(request.values.get("perms"))

        PermissionCRUD.grant(rid, perms, resource_id=resource_id)

        return self.jsonify(rid=rid, resource_id=resource_id, perms=perms)


class RolePermissionBatchGrantView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/batch/grant',
                  '/roles/<int:rid>/resource_groups/batch/grant')

    @auth_only_for_acl
    def post(self, rid):
        resource_ids = request.values.get('resource_ids')
        group_ids = request.values.get('group_ids')

        perms = handle_arg_list(request.values.get("perms"))

        if resource_ids and isinstance(resource_ids, list):
            for resource_id in resource_ids[:-1]:
                PermissionCRUD.grant(rid, perms, resource_id=resource_id, group_id=None, rebuild=False)
            PermissionCRUD.grant(rid, perms, resource_id=resource_ids[-1], group_id=None, rebuild=True)

        if group_ids and isinstance(group_ids, list):
            for group_id in group_ids[:-1]:
                PermissionCRUD.grant(rid, perms, resource_id=None, group_id=group_id, rebuild=False)
            PermissionCRUD.grant(rid, perms, resource_id=None, group_id=group_ids[-1], rebuild=True)

        return self.jsonify(rid=rid, resource_ids=resource_ids, group_ids=group_ids, perms=perms)


class RolePermissionRevokeView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/revoke',
                  '/roles/<int:rid>/resource_groups/<int:group_id>/revoke',
                  '/roles/<int:rid>/resources/batch/revoke2',  # by names
                  )

    @auth_only_for_acl
    def post(self, rid, resource_id=None, group_id=None):
        perms = handle_arg_list(request.values.get("perms"))
        if "batch" in request.url:
            resource_names = request.values.get('resource_names')
            resource_type_id = request.values.get('resource_type_id')
            resource_ids = request.values.get('resource_ids')
            perm_map = request.values.get('perm_map')
            app = AppCache.get(request.values.get('app_id'))
            PermissionCRUD.batch_revoke_by_resource_names(rid, perms, resource_type_id, resource_names,
                                                          resource_ids, perm_map, app_id=app and app.id)

            return self.jsonify(rid=rid, resource_names=resource_names, resource_type_id=resource_type_id, perms=perms)

        PermissionCRUD.revoke(rid, perms, resource_id=resource_id, group_id=group_id)

        return self.jsonify(rid=rid, resource_id=resource_id, group_id=group_id, perms=perms)


class RolePermissionRevoke2View(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/revoke2',
                  '/roles/<int:rid>/resource_groups/<int:group_id>/revoke2',)

    def post(self, rid, resource_id=None, group_id=None):
        if not ACLManager(request.values.get('app_id')).has_permission(None, None, 'grant', resource_id):
            return abort(403, ErrFormat.no_permission2)

        perms = handle_arg_list(request.values.get("perms"))

        PermissionCRUD.revoke(rid, perms, resource_id=resource_id, group_id=group_id)

        return self.jsonify(rid=rid, resource_id=resource_id, perms=perms)


class RolePermissionBatchRevokeView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/batch/revoke',
                  '/roles/<int:rid>/resource_groups/batch/revoke')

    @auth_only_for_acl
    def post(self, rid):
        resource_ids = request.values.get('resource_ids')
        group_ids = request.values.get('group_ids')

        perms = handle_arg_list(request.values.get("perms"))

        if resource_ids and isinstance(resource_ids, list):
            for resource_id in resource_ids[:-1]:
                PermissionCRUD.revoke(rid, perms, resource_id=resource_id, group_id=None, rebuild=False)
            PermissionCRUD.revoke(rid, perms, resource_id=resource_ids[-1], group_id=None, rebuild=True)

        if group_ids and isinstance(group_ids, list):
            for group_id in group_ids[:-1]:
                PermissionCRUD.revoke(rid, perms, resource_id=None, group_id=group_id, rebuild=False)
            PermissionCRUD.revoke(rid, perms, resource_id=None, group_id=group_ids[-1], rebuild=True)

        return self.jsonify(rid=rid, resource_ids=resource_ids, group_ids=group_ids, perms=perms)
