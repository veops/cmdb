# -*- coding:utf-8 -*-

import itertools
import redis_lock
from flask import abort

from api.extensions import rd
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import BuiltinModelEnum
from api.lib.cmdb.dcim.base import DCIMBase
from api.lib.cmdb.dcim.const import OperateTypeEnum
from api.lib.cmdb.dcim.const import RackBuiltinAttributes
from api.lib.cmdb.dcim.history import OperateHistoryManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.search.ci.db.search import Search as SearchFromDB
from api.lib.cmdb.search.ci_relation.search import Search as RelationSearch


class RackManager(DCIMBase):
    def __init__(self):
        super(RackManager, self).__init__()

        self.ci_type = CITypeCache.get(BuiltinModelEnum.DCIM_RACK) or abort(
            404, ErrFormat.dcim_builtin_model_not_found.format(BuiltinModelEnum.DCIM_RACK))

        self.type_id = self.ci_type.id

    @classmethod
    def update(cls, _id, **kwargs):
        if RackBuiltinAttributes.U_COUNT in kwargs:
            devices, _, _, _, _, _ = RelationSearch(
                [_id],
                level=[1],
                fl=[RackBuiltinAttributes.U_COUNT, RackBuiltinAttributes.U_START],
                count=1000000).search()
            for device in devices:
                u_start = device.get(RackBuiltinAttributes.U_START)
                u_count = device.get(RackBuiltinAttributes.U_COUNT) or 2
                if u_start and u_start + u_count - 1 > kwargs[RackBuiltinAttributes.U_COUNT]:
                    return abort(400, ErrFormat.dcim_rack_u_count_invalid)

        CIManager().update(_id, _sync=True, **kwargs)

        if RackBuiltinAttributes.U_COUNT in kwargs:
            payload = {RackBuiltinAttributes.FREE_U_COUNT: cls.calc_u_free_count(_id)}

            CIManager().update(_id, _sync=True, **payload)

    def delete(self, _id):
        super(RackManager, self).delete(_id)

        payload = {RackBuiltinAttributes.U_START: None}
        _, _, second_cis = CIRelationManager.get_second_cis(_id, per_page='all')
        for ci in second_cis:
            CIManager().update(ci['_id'], **payload)

    @staticmethod
    def calc_u_free_count(rack_id, device_id=None, u_start=None, u_count=None):
        rack = CIManager.get_ci_by_id(rack_id, need_children=False)
        if not rack.get(RackBuiltinAttributes.U_COUNT):
            return 0

        if device_id is not None and u_count is None:
            ci = CIManager().get_ci_by_id(device_id, need_children=False)
            u_count = ci.get(RackBuiltinAttributes.U_COUNT) or 2

        if u_start and u_start + u_count - 1 > rack.get(RackBuiltinAttributes.U_COUNT):
            return abort(400, ErrFormat.dcim_rack_u_slot_invalid)

        devices, _, _, _, _, _ = RelationSearch(
            [rack_id],
            level=[1],
            fl=[RackBuiltinAttributes.U_COUNT, RackBuiltinAttributes.U_START],
            count=1000000).search()

        u_count_sum = 0
        for device in devices:
            u_count_sum += (device.get(RackBuiltinAttributes.U_COUNT) or 2)
            if device_id is not None:
                _u_start = device.get(RackBuiltinAttributes.U_START)
                _u_count = device.get(RackBuiltinAttributes.U_COUNT) or 2
                if not _u_start:
                    continue

                if device.get('_id') != device_id and set(range(u_start, u_start + u_count)) & set(
                        range(_u_start, _u_start + _u_count)):
                    return abort(400, ErrFormat.dcim_rack_u_slot_invalid)

        return rack[RackBuiltinAttributes.U_COUNT] - u_count_sum

    def check_u_slot(self):
        racks, _, _, _, _, _ = SearchFromDB(
            "_type:{}".format(self.type_id),
            count=10000000,
            fl=[RackBuiltinAttributes.U_START, RackBuiltinAttributes.U_COUNT, RackBuiltinAttributes.U_SLOT_ABNORMAL],
            parent_node_perm_passed=True).search()

        for rack in racks:
            devices, _, _, _, _, _ = RelationSearch(
                [rack['_id']],
                level=[1],
                fl=[RackBuiltinAttributes.U_COUNT, RackBuiltinAttributes.U_START],
                count=1000000).search()

            u_slot_sets = []
            for device in devices:
                u_start = device.get(RackBuiltinAttributes.U_START)
                u_count = device.get(RackBuiltinAttributes.U_COUNT) or 2
                if u_start is not None and str(u_start).isdigit():
                    u_slot_sets.append(set(range(u_start, u_start + u_count)))

            if len(u_slot_sets) > 1:
                u_slot_abnormal = False
                for a, b in itertools.combinations(u_slot_sets, 2):
                    if a.intersection(b):
                        u_slot_abnormal = True
                        break
                if u_slot_abnormal != rack.get(RackBuiltinAttributes.U_SLOT_ABNORMAL):
                    payload = {RackBuiltinAttributes.U_SLOT_ABNORMAL: u_slot_abnormal}
                    CIManager().update(rack['_id'], **payload)

    def add_device(self, rack_id, device_id, u_start, u_count=None):
        with (redis_lock.Lock(rd.r, "DCIM_RACK_OPERATE_{}".format(rack_id))):
            self.calc_u_free_count(rack_id, device_id, u_start, u_count)

            self.add_relation(rack_id, device_id)

            payload = {RackBuiltinAttributes.U_START: u_start}
            if u_count:
                payload[RackBuiltinAttributes.U_COUNT] = u_count
            CIManager().update(device_id, _sync=True, **payload)

            payload = {
                RackBuiltinAttributes.FREE_U_COUNT: self.calc_u_free_count(rack_id, device_id, u_start, u_count)}
            CIManager().update(rack_id, _sync=True, **payload)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.ADD_DEVICE, rack_id=rack_id, ci_id=device_id)

    def remove_device(self, rack_id, device_id):
        with (redis_lock.Lock(rd.r, "DCIM_RACK_OPERATE_{}".format(rack_id))):
            CIRelationManager.delete_3(rack_id, device_id, apply_async=False, valid=False)

            payload = {RackBuiltinAttributes.FREE_U_COUNT: self.calc_u_free_count(rack_id)}
            CIManager().update(rack_id, _sync=True, **payload)

            payload = {RackBuiltinAttributes.U_START: None}
            CIManager().update(device_id, _sync=True, **payload)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.REMOVE_DEVICE, rack_id=rack_id, ci_id=device_id)

    def move_device(self, rack_id, device_id, to_u_start):
        with (redis_lock.Lock(rd.r, "DCIM_RACK_OPERATE_{}".format(rack_id))):
            payload = {RackBuiltinAttributes.FREE_U_COUNT: self.calc_u_free_count(rack_id, device_id, to_u_start)}
            CIManager().update(rack_id, _sync=True, **payload)

            CIManager().update(device_id, _sync=True, **{RackBuiltinAttributes.U_START: to_u_start})

        OperateHistoryManager().add(operate_type=OperateTypeEnum.MOVE_DEVICE, rack_id=rack_id, ci_id=device_id)

    def migrate_device(self, rack_id, device_id, to_rack_id, to_u_start):
        with (redis_lock.Lock(rd.r, "DCIM_RACK_OPERATE_{}".format(rack_id))):
            self.calc_u_free_count(to_rack_id, device_id, to_u_start)

            if rack_id != to_rack_id:
                CIRelationManager.delete_3(rack_id, device_id, apply_async=False, valid=False)

                self.add_relation(to_rack_id, device_id)

                payload = {
                    RackBuiltinAttributes.FREE_U_COUNT: self.calc_u_free_count(to_rack_id, device_id, to_u_start)}
                CIManager().update(to_rack_id, _sync=True, **payload)

            CIManager().update(device_id, _sync=True, **{RackBuiltinAttributes.U_START: to_u_start})

            if rack_id != to_rack_id:
                payload = {RackBuiltinAttributes.FREE_U_COUNT: self.calc_u_free_count(rack_id)}
                CIManager().update(rack_id, _sync=True, **payload)

        OperateHistoryManager().add(operate_type=OperateTypeEnum.REMOVE_DEVICE, rack_id=rack_id, ci_id=device_id)
        OperateHistoryManager().add(operate_type=OperateTypeEnum.ADD_DEVICE, rack_id=to_rack_id, ci_id=device_id)
