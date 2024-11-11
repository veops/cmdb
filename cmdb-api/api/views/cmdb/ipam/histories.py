# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.ipam.history import OperateHistoryManager
from api.lib.cmdb.ipam.history import ScanHistoryManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView

app_cli = CMDBApp()


class IPAMOperateHistoryView(APIView):
    url_prefix = ("/ipam/history/operate",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self):
        page = get_page(request.values.pop("page", 1))
        page_size = get_page_size(request.values.pop("page_size", None))
        operate_type = handle_arg_list(request.values.pop('operate_type', []))
        if operate_type:
            request.values["operate_type"] = operate_type

        numfound, result = OperateHistoryManager.search(page, page_size, **request.values)

        return self.jsonify(numfound=numfound, result=result)


class IPAMScanHistoryView(APIView):
    url_prefix = ("/ipam/history/scan",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.IPAM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self):
        page = get_page(request.values.pop("page", 1))
        page_size = get_page_size(request.values.pop("page_size", None))

        numfound, result = ScanHistoryManager.search(page, page_size, **request.values)

        return self.jsonify(numfound=numfound, result=result)

    @args_required("exec_id")
    def post(self):

        ScanHistoryManager().add(**request.values)

        return self.jsonify(code=200)
