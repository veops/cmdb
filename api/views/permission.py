# -*- coding:utf-8 -*-

from flask import request
from flask import session
from flask_login import current_user

from api.lib.decorator import args_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import validate_permission
from api.resource import APIView


class HasPermissionView(APIView):
    url_prefix = "/validate"

    @args_required("resource")
    @args_required("resource_type")
    @args_required("perm")
    def get(self):
        resource = request.values.get("resource")
        resource_type = request.values.get("resource_type")
        perm = request.values.get("perm")
        validate_permission(resource, resource_type, perm)
        return self.jsonify(is_valid=True)

    def post(self):
        self.get()


class GetResourcesView(APIView):
    url_prefix = "/resources"

    @args_required("resource_type")
    def get(self):
        resource_type = request.values.get("resource_type")
        res = ACLManager().get_resources(resource_type)
        return self.jsonify(res)


class GetUserInfoView(APIView):
    url_prefix = "/user/info"

    def get(self):
        name = session.get("acl", {}).get("nickName") or session.get("CAS_USERNAME") or current_user.nickname
        role = dict(permissions=session.get("acl", {}).get("parentRoles", []) or ["admin"])
        avatar = session.get("acl", {}).get("avatar") or current_user.avatar
        return self.jsonify(result=dict(name=name,
                                        role=role,
                                        avatar=avatar))
