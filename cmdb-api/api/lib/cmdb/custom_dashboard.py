# -*- coding:utf-8 -*-

from flask import abort

from api.lib.cmdb.resp_format import ErrFormat
from api.models.cmdb import CustomDashboard
from api.models.cmdb import SystemConfig


class CustomDashboardManager(object):
    cls = CustomDashboard

    @staticmethod
    def get():
        return sorted(CustomDashboard.get_by(to_dict=True), key=lambda x: (x["category"], x['order']))

    @staticmethod
    def preview(**kwargs):
        from api.lib.cmdb.cache import CMDBCounterCache

        res = CMDBCounterCache.update(kwargs, flush=False)

        return res

    @staticmethod
    def add(**kwargs):
        from api.lib.cmdb.cache import CMDBCounterCache

        if kwargs.get('name'):
            CustomDashboard.get_by(name=kwargs['name']) and abort(400, ErrFormat.custom_name_duplicate)

        new = CustomDashboard.create(**kwargs)

        res = CMDBCounterCache.update(new.to_dict())

        return new, res

    @staticmethod
    def update(_id, **kwargs):
        from api.lib.cmdb.cache import CMDBCounterCache

        existed = CustomDashboard.get_by_id(_id) or abort(404, ErrFormat.not_found)

        new = existed.update(**kwargs)

        res = CMDBCounterCache.update(new.to_dict())

        return new, res

    @staticmethod
    def batch_update(id2options):
        for _id in id2options:
            existed = CustomDashboard.get_by_id(_id) or abort(404, ErrFormat.not_found)
            existed.update(options=id2options[_id])

    @staticmethod
    def delete(_id):
        existed = CustomDashboard.get_by_id(_id) or abort(404, ErrFormat.not_found)

        existed.soft_delete()


class SystemConfigManager(object):
    cls = SystemConfig

    @staticmethod
    def get(name):
        return SystemConfig.get_by(name=name, first=True, to_dict=True)

    @staticmethod
    def create_or_update(name, option):
        existed = SystemConfig.get_by(name=name, first=True, to_dict=False)
        if existed is not None:
            return existed.update(option=option)
        else:
            return SystemConfig.create(name=name, option=option)

    @staticmethod
    def delete(name):
        existed = SystemConfig.get_by(name=name, first=True, to_dict=False) or abort(404, ErrFormat.not_found)

        existed.soft_delete()
