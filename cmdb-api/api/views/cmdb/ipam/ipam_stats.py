# -*- coding:utf-8 -*-


from flask import request

from api.lib.cmdb.ipam.stats import Stats
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.resource import APIView

app_cli = CMDBApp()


class IPAMStatsView(APIView):
    url_prefix = '/ipam/stats'

    @args_required("parent_id")
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self):
        parent_id = request.values.get("parent_id")

        return self.jsonify(Stats().summary(parent_id))
