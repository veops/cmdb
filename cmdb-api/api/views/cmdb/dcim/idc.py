# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.dcim.idc import IDCManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.resource import APIView

app_cli = CMDBApp()


class IDCView(APIView):
    url_prefix = ("/dcim/idc", "/dcim/idc/<int:_id>")

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        parent_id = request.values.pop("parent_id")

        return self.jsonify(ci_id=IDCManager().add(parent_id, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        IDCManager().update(_id, **request.values)

        return self.jsonify(ci_id=_id)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        IDCManager().delete(_id)

        return self.jsonify(ci_id=_id)
