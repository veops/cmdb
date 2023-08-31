from flask import abort

from api.extensions import db
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import CommonData


class CommonDataCRUD(object):

    @staticmethod
    def get_data_by_type(data_type):
        return CommonData.get_by(data_type=data_type)

    @staticmethod
    def get_data_by_id(_id, to_dict=True):
        return CommonData.get_by(first=True, id=_id, to_dict=to_dict)

    @staticmethod
    def create_new_data(data_type, **kwargs):
        try:
            return CommonData.create(data_type=data_type, **kwargs)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def update_data(_id, **kwargs):
        existed = CommonDataCRUD.get_data_by_id(_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))
        try:
            return existed.update(**kwargs)
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @staticmethod
    def delete(_id):
        existed = CommonDataCRUD.get_data_by_id(_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.common_data_not_found.format(_id))
        try:
            existed.soft_delete()
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))
