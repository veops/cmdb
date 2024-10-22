# -*- coding:utf-8 -*- 


from flask_babel import lazy_gettext as _l

from api.lib.utils import BaseEnum


class ValueTypeEnum(BaseEnum):
    INT = "0"
    FLOAT = "1"
    TEXT = "2"
    DATETIME = "3"
    DATE = "4"
    TIME = "5"
    JSON = "6"
    PASSWORD = TEXT
    LINK = TEXT
    BOOL = "7"
    REFERENCE = INT


class ConstraintEnum(BaseEnum):
    One2Many = "0"
    One2One = "1"
    Many2Many = "2"


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


class CITypeOperateType(BaseEnum):
    ADD = "0"  # add CIType
    UPDATE = "1"  # update CIType
    DELETE = "2"  # delete CIType
    ADD_ATTRIBUTE = "3"
    UPDATE_ATTRIBUTE = "4"
    DELETE_ATTRIBUTE = "5"
    ADD_TRIGGER = "6"
    UPDATE_TRIGGER = "7"
    DELETE_TRIGGER = "8"
    ADD_UNIQUE_CONSTRAINT = "9"
    UPDATE_UNIQUE_CONSTRAINT = "10"
    DELETE_UNIQUE_CONSTRAINT = "11"
    ADD_RELATION = "12"
    DELETE_RELATION = "13"
    ADD_RECONCILIATION = "14"
    UPDATE_RECONCILIATION = "15"
    DELETE_RECONCILIATION = "16"


class RetKey(BaseEnum):
    ID = "id"
    NAME = "name"
    ALIAS = "alias"


class ResourceTypeEnum(BaseEnum):
    CI = "CIType"
    CI_TYPE = "CIType"  # create/update/delete/read/config/grant
    CI_TYPE_RELATION = "CITypeRelation"  # create/delete/grant
    RELATION_VIEW = "RelationView"  # read/update/delete/grant
    CI_FILTER = "CIFilter"  # read
    PAGE = "page"  # read
    TOPOLOGY_VIEW = "TopologyView"  # read/update/delete/grant


class PermEnum(BaseEnum):
    ADD = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    CONFIG = "config"
    GRANT = "grant"


class RoleEnum(BaseEnum):
    CONFIG = "cmdb_admin"
    CMDB_READ_ALL = "CMDB_READ_ALL"


class AutoDiscoveryType(BaseEnum):
    AGENT = "agent"
    SNMP = "snmp"
    HTTP = "http"  # cloud
    COMPONENTS = "components"


class AttributeDefaultValueEnum(BaseEnum):
    CREATED_AT = "$created_at"
    UPDATED_AT = "$updated_at"
    AUTO_INC_ID = "$auto_inc_id"


class ExecuteStatusEnum(BaseEnum):
    COMPLETED = '0'
    FAILED = '1'
    RUNNING = '2'


class RelationSourceEnum(BaseEnum):
    ATTRIBUTE_VALUES = "0"
    AUTO_DISCOVERY = "1"


BUILTIN_ATTRIBUTES = {
    "_updated_at": _l("Update Time"),
    "_updated_by": _l("Updated By"),
}

CMDB_QUEUE = "one_cmdb_async"
REDIS_PREFIX_CI = "ONE_CMDB"
REDIS_PREFIX_CI_RELATION = "CMDB_CI_RELATION"
REDIS_PREFIX_CI_RELATION2 = "CMDB_CI_RELATION2"

BUILTIN_KEYWORDS = {'id', '_id', 'ci_id', 'type', '_type', 'ci_type', 'ticket_id', *BUILTIN_ATTRIBUTES.keys()}

L_TYPE = None
L_CI = None
