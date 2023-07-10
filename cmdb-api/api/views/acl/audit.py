# -*- coding:utf-8 -*-

from flask import request, abort

from api.lib.perm.acl.audit import AuditCRUD
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class AuditLogView(APIView):
    url_prefix = ("/audit_log/<string:name>",)

    def get(self, name):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        app_id = request.values.get('app_id')
        q = request.values.get('q')
        start = request.values.get('start')
        end = request.values.get('end')

        func_map = {
            'permission': AuditCRUD.search_permission,
            'role': AuditCRUD.search_role,
            'trigger': AuditCRUD.search_trigger,
            'resource': AuditCRUD.search_resource,
        }
        if name not in func_map:
            abort(400, f'wrong {name}, please use {func_map.keys()}')

        _func = func_map[name]

        data = _func(app_id, q, page, page_size, start, end)

        return self.jsonify(
            page=page,
            page_size=page_size,
            **data,
        )
