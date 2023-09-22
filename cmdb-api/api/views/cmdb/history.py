# -*- coding:utf-8 -*- 


import datetime

from flask import abort
from flask import request
from flask import session

from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.history import CITriggerHistoryManager
from api.lib.cmdb.history import CITypeHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import role_required
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class RecordView(APIView):
    url_prefix = ("/history/records/attribute", "/history/records/relation")

    @role_required(RoleEnum.CONFIG)
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        _start = request.values.get("start")
        _end = request.values.get("end")
        username = request.values.get("username", "")
        operate_type = request.values.get("operate_type", "")
        type_id = request.values.get("type_id")
        start, end = None, None
        if _start:
            try:
                start = datetime.datetime.strptime(_start, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return abort(400, ErrFormat.datetime_argument_invalid.format('start'))
        if _end:
            try:
                end = datetime.datetime.strptime(_end, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return abort(400, ErrFormat.datetime_argument_invalid.format('start'))

        if "attribute" in request.url:
            total, res = AttributeHistoryManger.get_records_for_attributes(start, end, username, page, page_size,
                                                                           operate_type,
                                                                           type_id,
                                                                           request.values.get('ci_id'),
                                                                           request.values.get('attr_id'))
            return self.jsonify(records=res,
                                total=total,
                                **request.values)
        else:
            total, res, cis = AttributeHistoryManger.get_records_for_relation(start, end, username, page, page_size,
                                                                              operate_type,
                                                                              type_id,
                                                                              request.values.get('first_ci_id'),
                                                                              request.values.get('second_ci_id'))

            return self.jsonify(records=res,
                                total=total,
                                cis=cis,
                                **request.values)


class CIHistoryView(APIView):
    url_prefix = "/history/ci/<int:ci_id>"

    @has_perm_from_args("ci_id", ResourceTypeEnum.CI, PermEnum.READ, CIManager.get_type_name)
    def get(self, ci_id):
        result = AttributeHistoryManger.get_by_ci_id(ci_id)

        return self.jsonify(result)


class CITriggerHistoryView(APIView):
    url_prefix = ("/history/ci_triggers/<int:ci_id>", "/history/ci_triggers")

    @has_perm_from_args("ci_id", ResourceTypeEnum.CI, PermEnum.READ, CIManager.get_type_name)
    def get(self, ci_id=None):
        if ci_id is not None:
            result = CITriggerHistoryManager.get_by_ci_id(ci_id)

            return self.jsonify(result)

        if RoleEnum.CONFIG not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin("cmdb"):
            return abort(403, ErrFormat.role_required.format(RoleEnum.CONFIG))

        type_id = request.values.get("type_id")
        trigger_id = request.values.get("trigger_id")
        operate_type = request.values.get("operate_type")

        page = get_page(request.values.get('page', 1))
        page_size = get_page_size(request.values.get('page_size', 1))

        numfound, result = CITriggerHistoryManager.get(page,
                                                       page_size,
                                                       type_id=type_id,
                                                       trigger_id=trigger_id,
                                                       operate_type=operate_type)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(result),
                            result=result)


class CITypeHistoryView(APIView):
    url_prefix = "/history/ci_types"

    @role_required(RoleEnum.CONFIG)
    def get(self):
        type_id = request.values.get("type_id")
        username = request.values.get("username")
        operate_type = request.values.get("operate_type")

        page = get_page(request.values.get('page', 1))
        page_size = get_page_size(request.values.get('page_size', 1))

        numfound, result = CITypeHistoryManager.get(page, page_size, username,
                                                    type_id=type_id, operate_type=operate_type)

        return self.jsonify(page=page,
                            page_size=page_size,
                            numfound=numfound,
                            total=len(result),
                            result=result)
