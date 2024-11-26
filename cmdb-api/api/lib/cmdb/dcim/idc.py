# -*- coding:utf-8 -*-


from flask import abort

from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.dcim.base import DCIMBase
from api.lib.cmdb.resp_format import ErrFormat


class IDCManager(DCIMBase):
    def __init__(self):
        super(IDCManager, self).__init__()

        self.ci_type = CITypeCache.get(BuiltinModelEnum.DCIM_IDC) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_IDC))

        self.type_id = self.ci_type.id
