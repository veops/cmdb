# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.dcim.history import OperateHistoryManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView

app_cli = CMDBApp()


class DCIMOperateHistoryView(APIView):
    url_prefix = ("/dcim/history/operate",)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.DCIM,
                         app_cli.op.read, app_cli.admin_name)
    def get(self):
        page = get_page(request.values.pop("page", 1))
        page_size = get_page_size(request.values.pop("page_size", None))
        operate_type = handle_arg_list(request.values.pop('operate_type', []))
        if operate_type:
            request.values["operate_type"] = operate_type

        numfound, result, id2ci, type2show_key = OperateHistoryManager.search(page, page_size, **request.values)

        return self.jsonify(numfound=numfound, result=result, id2ci=id2ci, type2show_key=type2show_key)
