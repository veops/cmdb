# -*- coding:utf-8 -*-


from flask import request

from api.lib.cmdb.custom_dashboard import CustomDashboardManager
from api.lib.cmdb.custom_dashboard import SystemConfigManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.resource import APIView

app_cli = CMDBApp()


class CustomDashboardApiView(APIView):
    url_prefix = ("/custom_dashboard", "/custom_dashboard/<int:_id>", "/custom_dashboard/batch",
                  "/custom_dashboard/preview")

    def get(self):
        return self.jsonify(CustomDashboardManager.get())

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Customized_Dashboard,
                         app_cli.op.read, app_cli.admin_name)
    @args_validate(CustomDashboardManager.cls)
    def post(self):
        if request.url.endswith("/preview"):
            return self.jsonify(counter=CustomDashboardManager.preview(**request.values))

        cm, counter = CustomDashboardManager.add(**request.values)

        res = cm.to_dict()
        res.update(counter=counter)

        return self.jsonify(res)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Customized_Dashboard,
                         app_cli.op.read, app_cli.admin_name)
    @args_validate(CustomDashboardManager.cls)
    def put(self, _id=None):
        if _id is not None:
            cm, counter = CustomDashboardManager.update(_id, **request.values)

            res = cm.to_dict()
            res.update(counter=counter)

            return self.jsonify(res)

        CustomDashboardManager.batch_update(request.values.get("id2options"))

        return self.jsonify(id2options=request.values.get('id2options'))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Customized_Dashboard,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, _id):
        CustomDashboardManager.delete(_id)

        return self.jsonify(code=200)


class SystemConfigApiView(APIView):
    url_prefix = ("/system_config",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Service_Tree_Definition,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("name", value_required=True)
    def get(self):
        return self.jsonify(SystemConfigManager.get(request.values['name']))

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Service_Tree_Definition,
                         app_cli.op.read, app_cli.admin_name)
    @args_validate(SystemConfigManager.cls)
    @args_required("name", value_required=True)
    @args_required("option", value_required=True)
    def post(self):
        cm = SystemConfigManager.create_or_update(**request.values)

        return self.jsonify(cm.to_dict())

    def put(self, _id=None):
        return self.post()

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Service_Tree_Definition,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("name")
    def delete(self):
        CustomDashboardManager.delete(request.values['name'])

        return self.jsonify(code=200)
