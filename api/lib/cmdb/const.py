# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

import datetime

import six
from markupsafe import escape

from api.lib.cmdb.cache import AttributeCache
from api.models.cmdb import Attribute
from api.models.cmdb import CIIndexValueDateTime
from api.models.cmdb import CIIndexValueFloat
from api.models.cmdb import CIIndexValueInteger
from api.models.cmdb import CIIndexValueText
from api.models.cmdb import CIValueDateTime
from api.models.cmdb import CIValueFloat
from api.models.cmdb import CIValueInteger
from api.models.cmdb import CIValueText
from api.models.cmdb import FloatChoice
from api.models.cmdb import IntegerChoice
from api.models.cmdb import TextChoice


def string2int(x):
    return int(float(x))


def str2datetime(x):
    try:
        return datetime.datetime.strptime(x, "%Y-%m-%d")
    except ValueError:
        pass

    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


type_map = {
    'deserialize': {
        Attribute.INT: string2int,
        Attribute.FLOAT: float,
        Attribute.TEXT: lambda x: escape(x).encode('utf-8').decode('utf-8'),
        Attribute.TIME: lambda x: escape(x).encode('utf-8').decode('utf-8'),
        Attribute.DATETIME: str2datetime,
        Attribute.DATE: str2datetime,
    },
    'serialize': {
        Attribute.INT: int,
        Attribute.FLOAT: float,
        Attribute.TEXT: lambda x: x if isinstance(x, six.text_type) else str(x),
        Attribute.TIME: lambda x: x if isinstance(x, six.text_type) else str(x),
        Attribute.DATE: lambda x: x.strftime("%Y-%m-%d"),
        Attribute.DATETIME: lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    },
    'serialize2': {
        Attribute.INT: int,
        Attribute.FLOAT: float,
        Attribute.TEXT: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        Attribute.TIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        Attribute.DATE: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        Attribute.DATETIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
    },
    'choice': {
        Attribute.INT: IntegerChoice,
        Attribute.FLOAT: FloatChoice,
        Attribute.TEXT: TextChoice,
    },
    'table': {
        Attribute.INT: CIValueInteger,
        Attribute.TEXT: CIValueText,
        Attribute.DATETIME: CIValueDateTime,
        Attribute.DATE: CIValueDateTime,
        Attribute.TIME: CIValueText,
        Attribute.FLOAT: CIValueFloat,
        'index_{0}'.format(Attribute.INT): CIIndexValueInteger,
        'index_{0}'.format(Attribute.TEXT): CIIndexValueText,
        'index_{0}'.format(Attribute.DATETIME): CIIndexValueDateTime,
        'index_{0}'.format(Attribute.DATE): CIIndexValueDateTime,
        'index_{0}'.format(Attribute.TIME): CIIndexValueText,
        'index_{0}'.format(Attribute.FLOAT): CIIndexValueFloat,
    },
    'table_name': {
        Attribute.INT: 'c_value_integers',
        Attribute.TEXT: 'c_value_texts',
        Attribute.DATETIME: 'c_value_datetime',
        Attribute.DATE: 'c_value_datetime',
        Attribute.TIME: 'c_value_texts',
        Attribute.FLOAT: 'c_value_floats',
        'index_{0}'.format(Attribute.INT): 'c_value_index_integers',
        'index_{0}'.format(Attribute.TEXT): 'c_value_index_texts',
        'index_{0}'.format(Attribute.DATETIME): 'c_value_index_datetime',
        'index_{0}'.format(Attribute.DATE): 'c_value_index_datetime',
        'index_{0}'.format(Attribute.TIME): 'c_value_index_texts',
        'index_{0}'.format(Attribute.FLOAT): 'c_value_index_floats',
    },
    'es_type': {
        Attribute.INT: 'long',
        Attribute.TEXT: 'text',
        Attribute.DATETIME: 'text',
        Attribute.DATE: 'text',
        Attribute.TIME: 'text',
        Attribute.FLOAT: 'float'
    }
}


class TableMap(object):
    def __init__(self, attr_name=None):
        self.attr_name = attr_name

    @property
    def table(self):
        attr = AttributeCache.get(self.attr_name)
        i = "index_{0}".format(attr.value_type) if attr.is_index else attr.value_type
        return type_map["table"].get(i)

    @property
    def table_name(self):
        attr = AttributeCache.get(self.attr_name)
        i = "index_{0}".format(attr.value_type) if attr.is_index else attr.value_type
        return type_map["table_name"].get(i)


class ExistPolicy(object):
    REJECT = "reject"
    NEED = "need"
    IGNORE = "ignore"
    REPLACE = "replace"


class OperateType(object):
    ADD = "0"
    DELETE = "1"
    UPDATE = "2"


class RetKey(object):
    ID = "id"
    NAME = "name"
    ALIAS = "alias"


class ResourceType(object):
    CI = "CIType"


class PermEnum(object):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"


class RoleEnum(object):
    CONFIG = "admin"


CMDB_QUEUE = "cmdb_async"
REDIS_PREFIX = "CMDB_CI"
