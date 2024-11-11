# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.ipam.subnet import SubnetManager
from api.lib.cmdb.ipam.subnet import SubnetScopeManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.resource import APIView

app_cli = CMDBApp()


class SubnetView(APIView):
    url_prefix = ("/ipam/subnet", "/ipam/subnet/hosts", "/ipam/subnet/<int:_id>")

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self, _id=None):
        if "hosts" in request.url:
            return self.jsonify(SubnetManager.get_hosts(request.values.get('cidr')))

        if _id is not None:
            return self.jsonify(SubnetManager().get_by_id(_id))

        result, type2name = SubnetManager().tree_view()

        return self.jsonify(result=result, type2name=type2name)

    @args_required("cidr")
    @args_required("parent_id", value_required=False)
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        cidr = request.values.pop("cidr")
        parent_id = request.values.pop("parent_id")
        agent_id = request.values.pop("agent_id", None)
        cron = request.values.pop("cron", None)

        return self.jsonify(SubnetManager().add(cidr, parent_id, agent_id, cron, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        return self.jsonify(id=SubnetManager().update(_id, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        return self.jsonify(id=SubnetManager().delete(_id))


class SubnetScopeView(APIView):
    url_prefix = ("/ipam/scope", "/ipam/scope/<int:_id>")

    @args_required("parent_id", value_required=False)
    @args_required("name")
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def post(self):
        parent_id = request.values.pop("parent_id")
        name = request.values.pop("name")

        return self.jsonify(SubnetScopeManager().add(parent_id, name))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def put(self, _id):
        return self.jsonify(id=SubnetScopeManager().update(_id, **request.values))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        return self.jsonify(id=SubnetScopeManager.delete(_id))
