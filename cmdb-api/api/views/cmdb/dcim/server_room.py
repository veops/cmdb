# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.dcim.server_room import ServerRoomManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.resource import APIView

app_cli = CMDBApp()


class ServerRoomView(APIView):
    url_prefix = ("/dcim/server_room", "/dcim/server_room/<int:_id>", "/dcim/server_room/<int:_id>/racks")

    def get(self, _id):
        q = request.values.get('q')
        counter, result = ServerRoomManager.get_racks(_id, q)

        return self.jsonify(counter=counter, result=result)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("parent_id")
    def post(self):
        parent_id = request.values.pop("parent_id")

        return self.jsonify(ci_id=ServerRoomManager().add(parent_id, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        ServerRoomManager().update(_id, **request.values)

        return self.jsonify(ci_id=_id)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        ServerRoomManager().delete(_id)

        return self.jsonify(ci_id=_id)
