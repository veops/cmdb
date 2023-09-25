# -*- coding:utf-8 -*-


from flask import request

from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.custom_dashboard import CustomDashboardManager
from api.lib.cmdb.custom_dashboard import SystemConfigManager
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import role_required
from api.resource import APIView


class CustomDashboardApiView(APIView):
    url_prefix = ("/custom_dashboard", "/custom_dashboard/<int:_id>", "/custom_dashboard/batch",
                  "/custom_dashboard/preview")

    def get(self):
        return self.jsonify(CustomDashboardManager.get())

    @role_required(RoleEnum.CONFIG)
    @args_validate(CustomDashboardManager.cls)
    def post(self):
        if request.url.endswith("/preview"):
            return self.jsonify(counter=CustomDashboardManager.preview(**request.values))

        cm, counter = CustomDashboardManager.add(**request.values)

        res = cm.to_dict()
        res.update(counter=counter)

        return self.jsonify(res)

    @role_required(RoleEnum.CONFIG)
    @args_validate(CustomDashboardManager.cls)
    def put(self, _id=None):
        if _id is not None:
            cm, counter = CustomDashboardManager.update(_id, **request.values)

            res = cm.to_dict()
            res.update(counter=counter)

            return self.jsonify(res)

        CustomDashboardManager.batch_update(request.values.get("id2options"))

        return self.jsonify(id2options=request.values.get('id2options'))

    @role_required(RoleEnum.CONFIG)
    def delete(self, _id):
        CustomDashboardManager.delete(_id)

        return self.jsonify(code=200)


class SystemConfigApiView(APIView):
    url_prefix = ("/system_config",)

    @role_required(RoleEnum.CONFIG)
    @args_required("name", value_required=True)
    def get(self):
        return self.jsonify(SystemConfigManager.get(request.values['name']))

    @role_required(RoleEnum.CONFIG)
    @args_validate(SystemConfigManager.cls)
    @args_required("name", value_required=True)
    @args_required("option", value_required=True)
    def post(self):
        cm = SystemConfigManager.create_or_update(**request.values)

        return self.jsonify(cm.to_dict())

    def put(self, _id=None):
        return self.post()

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    def delete(self):
        CustomDashboardManager.delete(request.values['name'])

        return self.jsonify(code=200)
