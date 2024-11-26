# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.dcim.region import RegionManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.resource import APIView

app_cli = CMDBApp()


class RegionView(APIView):
    url_prefix = ("/dcim/region", "/dcim/region/<int:_id>")

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        return self.jsonify(ci_id=RegionManager().add(**request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        RegionManager().update(_id, **request.values)

        return self.jsonify(ci_id=_id)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        RegionManager().delete(_id)

        return self.jsonify(ci_id=_id)
