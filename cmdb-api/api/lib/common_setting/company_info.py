# -*- coding:utf-8 -*-
from urllib.parse import urlparse

from api.extensions import cache
from api.models.common_setting import CompanyInfo


class CompanyInfoCRUD(object):

    @staticmethod
    def get():
        return CompanyInfo.get_by(first=True) or {}

    @staticmethod
    def create(**kwargs):
        CompanyInfoCRUD.check_data(**kwargs)
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
            CompanyInfoCRUD.check_data(**kwargs)
            existed = existed.update(**kwargs)
        CompanyInfoCache.refresh(existed.info)
        return existed

    @staticmethod
    def check_data(**kwargs):
        info = kwargs.get('info', {})
        info['messenger'] = CompanyInfoCRUD.check_messenger(info.get('messenger', None))

        kwargs['info'] = info

    @staticmethod
    def check_messenger(messenger):
        if not messenger:
            return messenger

        parsed_url = urlparse(messenger)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"


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
