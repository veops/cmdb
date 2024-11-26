# -*- coding:utf-8 -*-


from flask import abort

from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.resp_format import ErrFormat


class RegionManager(object):
    def __init__(self):
        self.ci_type = CITypeCache.get(BuiltinModelEnum.DCIM_REGION) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_REGION))

        self.type_id = self.ci_type.id

    def add(self, **kwargs):
        return CIManager().add(self.type_id, exist_policy=ExistPolicy.REJECT, **kwargs)

    @classmethod
    def update(cls, _id, **kwargs):
        CIManager().update(_id, **kwargs)

    @classmethod
    def delete(cls, _id):
        CIManager().delete(_id)
