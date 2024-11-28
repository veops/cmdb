# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.dcim.const import RackBuiltinAttributes
from api.lib.cmdb.dcim.rack import RackManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.resource import APIView
from api.tasks.cmdb import dcim_calc_u_free_count

app_cli = CMDBApp()


class RackView(APIView):
    url_prefix = ("/dcim/rack", "/dcim/rack/<int:_id>")

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("parent_id")
    def post(self):
        parent_id = request.values.pop("parent_id")

        return self.jsonify(ci_id=RackManager().add(parent_id, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        RackManager().update(_id, **request.values)

        return self.jsonify(ci_id=_id)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        RackManager().delete(_id)

        return self.jsonify(ci_id=_id)


class RackDetailView(APIView):
    url_prefix = ("/dcim/rack/<int:rack_id>/device/<int:device_id>",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    @args_required(RackBuiltinAttributes.U_START)
    def post(self, rack_id, device_id):
        u_start = request.values.pop(RackBuiltinAttributes.U_START)
        u_count = request.values.get(RackBuiltinAttributes.U_COUNT)

        RackManager().add_device(rack_id, device_id, u_start, u_count)

        return self.jsonify(rack_id=rack_id, device_id=device_id)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("to_u_start")
    def put(self, rack_id, device_id):
        to_u_start = request.values.pop("to_u_start")

        RackManager().move_device(rack_id, device_id, to_u_start)

        return self.jsonify(rack_id=rack_id, device_id=device_id, to_u_start=to_u_start)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, rack_id, device_id):
        RackManager().remove_device(rack_id, device_id)

        return self.jsonify(code=200)


class RackDeviceMigrateView(APIView):
    url_prefix = ("/dcim/rack/<int:rack_id>/device/<int:device_id>/migrate",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("to_rack_id")
    @args_required("to_u_start")
    def put(self, rack_id, device_id):
        to_rack_id = request.values.pop("to_rack_id")
        to_u_start = request.values.pop("to_u_start")

        RackManager().migrate_device(rack_id, device_id, to_rack_id, to_u_start)

        return self.jsonify(rack_id=rack_id,
                            device_id=device_id,
                            to_u_start=to_u_start,
                            to_rack_id=to_rack_id)


class RackCalcUFreeCountView(APIView):
    url_prefix = ("/dcim/rack/calc_u_free_count",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        dcim_calc_u_free_count.apply_async(queue=CMDB_QUEUE)

        return self.jsonify(code=200)
