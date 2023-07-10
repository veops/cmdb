# -*- coding:utf-8 -*-
from flask import abort
from flask import request

from api.lib.common_setting.company_info import CompanyInfoCRUD
from api.lib.common_setting.resp_format import ErrFormat
from api.resource import APIView

prefix = '/company'


class CompanyInfoView(APIView):
    url_prefix = (f'{prefix}/info',)

    def get(self):
        return self.jsonify(CompanyInfoCRUD.get())

    def post(self):
        info = CompanyInfoCRUD.get()
        if info:
            abort(400, ErrFormat.company_info_is_already_existed)
        data = {
            'info': {
                **request.values
            }
        }
        d = CompanyInfoCRUD.create(**data)
        res = d.to_dict()
        return self.jsonify(res)


class CompanyInfoViewWithId(APIView):
    url_prefix = (f'{prefix}/info/<int:_id>',)

    def put(self, _id):
        data = {
            'info': {
                **request.values
            }
        }
        d = CompanyInfoCRUD.update(_id, **data)
        res = d.to_dict()
        return self.jsonify(res)
