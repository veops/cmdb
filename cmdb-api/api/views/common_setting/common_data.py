from flask import request

from api.lib.common_setting.common_data import CommonDataCRUD
from api.resource import APIView

prefix = '/data'


class DataView(APIView):
    url_prefix = (f'{prefix}/<string:data_type>',)

    def get(self, data_type):
        data_list = CommonDataCRUD.get_data_by_type(data_type)

        return self.jsonify(data_list)

    def post(self, data_type):
        params = request.json
        CommonDataCRUD.create_new_data(data_type, **params)

        return self.jsonify(params)


class DataViewWithId(APIView):
    url_prefix = (f'{prefix}/<string:data_type>/<int:_id>',)

    def put(self, _id):
        params = request.json
        res = CommonDataCRUD.update_data(_id, **params)

        return self.jsonify(res.to_dict())

    def delete(self, _id):
        CommonDataCRUD.delete(_id)
        return self.jsonify({})
