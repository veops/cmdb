# -*- coding:utf-8 -*-


from flask import abort

from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.dcim.base import DCIMBase
from api.lib.cmdb.dcim.const import RackBuiltinAttributes
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.models.cmdb import CI
from api.models.cmdb import CIRelation


class ServerRoomManager(DCIMBase):
    def __init__(self):
        super(ServerRoomManager, self).__init__()

        self.ci_type = CITypeCache.get(BuiltinModelEnum.DCIM_SERVER_ROOM) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_SERVER_ROOM))
        self.type_id = self.ci_type.id

    @staticmethod
    def get_racks(_id, q=None):
        rack_type = CITypeCache.get(BuiltinModelEnum.DCIM_RACK) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_RACK))

        relations = CIRelation.get_by(first_ci_id=_id, only_query=True).join(
            CI, CI.id == CIRelation.second_ci_id).filter(CI.type_id == rack_type.id)
        rack_ids = [i.second_ci_id for i in relations]

        q = "_type:{}".format(rack_type.id) if not q else "_type:{},{}".format(rack_type.id, q)
        if rack_ids:
            response, _, _, _, numfound, _ = SearchFromDB(
                q,
                ci_ids=list(rack_ids),
                count=1000000,
                parent_node_perm_passed=True).search()
        else:
            response, numfound = [], 0

        counter = dict(rack_count=numfound)
        u_count = 0
        free_u_count = 0
        for i in response:
            _u_count = i.get(RackBuiltinAttributes.U_COUNT) or 0
            u_count += _u_count
            free_u_count += (_u_count if i.get(RackBuiltinAttributes.FREE_U_COUNT) is None else
                             i.get(RackBuiltinAttributes.FREE_U_COUNT))
        counter["u_count"] = u_count
        counter["u_used_count"] = u_count - free_u_count
        counter["device_count"] = CIRelation.get_by(only_query=True).filter(
            CIRelation.first_ci_id.in_(rack_ids)).count()

        return counter, response
