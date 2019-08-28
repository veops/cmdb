# -*- coding:utf-8 -*- 


import datetime

from flask import abort
from flask import request

from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class RecordView(APIView):
    url_prefix = "/history/records"

    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        _start = request.values.get("start")
        _end = request.values.get("end")
        username = request.values.get("username", "")
        start, end = None, None
        if _start:
            try:
                start = datetime.datetime.strptime(_start, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                abort(400, 'incorrect start date time')
        if _end:
            try:
                end = datetime.datetime.strptime(_end, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                abort(400, 'incorrect end date time')

        numfound, total, res = AttributeHistoryManger.get_records(start, end, username, page, page_size)

        return self.jsonify(numfound=numfound,
                            records=res,
                            page=page,
                            total=total,
                            start=_start,
                            end=_end,
                            username=username)


class CIHistoryView(APIView):
    url_prefix = "/history/ci/<int:ci_id>"

    def get(self, ci_id):
        result = AttributeHistoryManger.get_by_ci_id(ci_id)
        return self.jsonify(result)


class RecordDetailView(APIView):
    url_prefix = "/history/records/<int:record_id>"

    def get(self, record_id):
        username, timestamp, attr_dict, rel_dict = AttributeHistoryManger.get_record_detail(record_id)
        return self.jsonify(username=username,
                            timestamp=timestamp,
                            attr_history=attr_dict,
                            rel_history=rel_dict)
