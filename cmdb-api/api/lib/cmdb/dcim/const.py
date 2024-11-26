# -*- coding:utf-8 -*-


from api.lib.utils import BaseEnum


class RackBuiltinAttributes(BaseEnum):
    U_COUNT = 'u_count'
    U_START = 'u_start'
    FREE_U_COUNT = 'free_u_count'
    U_SLOT_ABNORMAL = 'u_slot_abnormal'


class OperateTypeEnum(BaseEnum):
    ADD_DEVICE = "0"
    REMOVE_DEVICE = "1"
    MOVE_DEVICE = "2"
