# -*- coding:utf-8 -*-

from api.lib.utils import BaseEnum


class IPAddressAssignStatus(BaseEnum):
    ASSIGNED = 0
    UNASSIGNED = 1
    RESERVED = 2


class OperateTypeEnum(BaseEnum):
    ADD_SCOPE = "0"
    UPDATE_SCOPE = "1"
    DELETE_SCOPE = "2"
    ADD_SUBNET = "3"
    UPDATE_SUBNET = "4"
    DELETE_SUBNET = "5"
    ASSIGN_ADDRESS = "6"
    REVOKE_ADDRESS = "7"


class SubnetBuiltinAttributes(BaseEnum):
    NAME = 'name'
    CIDR = 'cidr'
    HOSTS_COUNT = 'hosts_count'
    ASSIGN_COUNT = 'assign_count'
    USED_COUNT = 'used_count'
    FREE_COUNT = 'free_count'


class IPAddressBuiltinAttributes(BaseEnum):
    IP = 'ip'
    ASSIGN_STATUS = 'assign_status'  # enum: 0 - assigned   1 - unassigned   2 - reserved
    IS_USED = 'is_used'  # bool
