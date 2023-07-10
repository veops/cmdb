# -*- coding:utf-8 -*-

from api.models.common_setting import CompanyInfo


class CompanyInfoCRUD(object):

    @staticmethod
    def get():
        return CompanyInfo.get_by(first=True) or {}

    @staticmethod
    def create(**kwargs):
        return CompanyInfo.create(**kwargs)

    @staticmethod
    def update(_id, **kwargs):
        kwargs.pop('id', None)
        existed = CompanyInfo.get_by_id(_id)
        if not existed:
            return CompanyInfoCRUD.create(**kwargs)
        else:
            existed = existed.update(**kwargs)
            return existed
