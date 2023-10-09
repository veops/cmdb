# -*- coding:utf-8 -*-
from api.extensions import cache
from api.models.common_setting import CompanyInfo


class CompanyInfoCRUD(object):

    @staticmethod
    def get():
        return CompanyInfo.get_by(first=True) or {}

    @staticmethod
    def create(**kwargs):
        res = CompanyInfo.create(**kwargs)
        CompanyInfoCache.refresh(res.info)
        return res

    @staticmethod
    def update(_id, **kwargs):
        kwargs.pop('id', None)
        existed = CompanyInfo.get_by_id(_id)
        if not existed:
            existed = CompanyInfoCRUD.create(**kwargs)
        else:
            existed = existed.update(**kwargs)
        CompanyInfoCache.refresh(existed.info)
        return existed


class CompanyInfoCache(object):
    key = 'CompanyInfoCache::'

    @classmethod
    def get(cls):
        info = cache.get(cls.key)
        if not info:
            res = CompanyInfo.get_by(first=True) or {}
            info = res.get('info', {})
            cache.set(cls.key, info)
        return info

    @classmethod
    def refresh(cls, info):
        cache.set(cls.key, info)