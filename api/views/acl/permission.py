# -*- coding:utf-8 -*-


from flask import request

from api.lib.decorator import args_required
from api.lib.perm.acl.permission import PermissionCRUD
from api.lib.utils import handle_arg_list
from api.resource import APIView


class ResourcePermissionView(APIView):
    url_prefix = ("/resources/<int:resource_id>/permissions", "/resource_groups/<int:group_id>/permissions")

    def get(self, resource_id=None, group_id=None):
        return self.jsonify(PermissionCRUD.get_all(resource_id, group_id))


class RolePermissionGrantView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/grant',
                  '/roles/<int:rid>/resource_groups/<int:group_id>/grant')

    @args_required('perms')
    def post(self, rid, resource_id=None, group_id=None):
        perms = handle_arg_list(request.values.get("perms"))
        PermissionCRUD.grant(rid, perms, resource_id=resource_id, group_id=group_id)

        return self.jsonify(rid=rid, resource_id=resource_id, group_id=group_id, perms=perms)


class RolePermissionRevokeView(APIView):
    url_prefix = ('/roles/<int:rid>/resources/<int:resource_id>/revoke',
                  '/roles/<int:rid>/resource_groups/<int:group_id>/revoke')

    @args_required('perms')
    def post(self, rid, resource_id=None, group_id=None):
        perms = handle_arg_list(request.values.get("perms"))
        PermissionCRUD.revoke(rid, perms, resource_id=resource_id, group_id=group_id)

        return self.jsonify(rid=rid, resource_id=resource_id, group_id=group_id, perms=perms)
