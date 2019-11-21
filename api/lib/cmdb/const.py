# -*- coding:utf-8 -*- 


from api.lib.utils import BaseEnum


class ValueTypeEnum(BaseEnum):
    INT = "0"
    FLOAT = "1"
    TEXT = "2"
    DATETIME = "3"
    DATE = "4"
    TIME = "5"


class CIStatusEnum(BaseEnum):
    REVIEW = "0"
    VALIDATE = "1"


class ExistPolicy(BaseEnum):
    REJECT = "reject"
    NEED = "need"
    IGNORE = "ignore"
    REPLACE = "replace"


class OperateType(BaseEnum):
    ADD = "0"
    DELETE = "1"
    UPDATE = "2"


class RetKey(BaseEnum):
    ID = "id"
    NAME = "name"
    ALIAS = "alias"


class ResourceType(BaseEnum):
    CI = "CIType"


class PermEnum(BaseEnum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"


class RoleEnum(BaseEnum):
    CONFIG = "admin"


CMDB_QUEUE = "cmdb_async"
REDIS_PREFIX_CI = "CMDB_CI"
REDIS_PREFIX_CI_RELATION = "CMDB_CI_RELATION"
