# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.ipam.address import IpAddressManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.lib.utils import handle_arg_list
from api.resource import APIView

app_cli = CMDBApp()


class IPAddressView(APIView):
    url_prefix = ("/ipam/address",)

    @args_required("parent_id")
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self):
        parent_id = request.args.get("parent_id")

        numfound, result = IpAddressManager.list_ip_address(parent_id)

        return self.jsonify(numfound=numfound, result=result)

    @args_required("ips")
    @args_required("assign_status", value_required=False)
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        ips = handle_arg_list(request.values.pop("ips"))
        parent_id = request.values.pop("parent_id", None)
        cidr = request.values.pop("cidr", None)

        IpAddressManager().assign_ips(ips, parent_id, cidr, **request.values)

        return self.jsonify(code=200)
