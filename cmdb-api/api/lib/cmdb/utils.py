# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import datetime

import six
from markupsafe import escape

import api.models.cmdb as model
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import ValueTypeEnum


def string2int(x):
    return int(float(x))


def str2datetime(x):
    try:
        return datetime.datetime.strptime(x, "%Y-%m-%d")
    except ValueError:
        pass

    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


class ValueTypeMap(object):
    deserialize = {
        ValueTypeEnum.INT: string2int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: escape(x).encode('utf-8').decode('utf-8'),
        ValueTypeEnum.TIME: lambda x: escape(x).encode('utf-8').decode('utf-8'),
        ValueTypeEnum.DATETIME: str2datetime,
        ValueTypeEnum.DATE: str2datetime,
    }

    serialize = {
        ValueTypeEnum.INT: int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: x if isinstance(x, six.text_type) else str(x),
        ValueTypeEnum.TIME: lambda x: x if isinstance(x, six.text_type) else str(x),
        ValueTypeEnum.DATE: lambda x: x.strftime("%Y-%m-%d"),
        ValueTypeEnum.DATETIME: lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
    }

    serialize2 = {
        ValueTypeEnum.INT: int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.TIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.DATE: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.DATETIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
    }

    choice = {
        ValueTypeEnum.INT: model.IntegerChoice,
        ValueTypeEnum.FLOAT: model.FloatChoice,
        ValueTypeEnum.TEXT: model.TextChoice,
    }

    table = {
        ValueTypeEnum.INT: model.CIValueInteger,
        ValueTypeEnum.TEXT: model.CIValueText,
        ValueTypeEnum.DATETIME: model.CIValueDateTime,
        ValueTypeEnum.DATE: model.CIValueDateTime,
        ValueTypeEnum.TIME: model.CIValueText,
        ValueTypeEnum.FLOAT: model.CIValueFloat,
        'index_{0}'.format(ValueTypeEnum.INT): model.CIIndexValueInteger,
        'index_{0}'.format(ValueTypeEnum.TEXT): model.CIIndexValueText,
        'index_{0}'.format(ValueTypeEnum.DATETIME): model.CIIndexValueDateTime,
        'index_{0}'.format(ValueTypeEnum.DATE): model.CIIndexValueDateTime,
        'index_{0}'.format(ValueTypeEnum.TIME): model.CIIndexValueText,
        'index_{0}'.format(ValueTypeEnum.FLOAT): model.CIIndexValueFloat,
    }

    table_name = {
        ValueTypeEnum.INT: 'c_value_integers',
        ValueTypeEnum.TEXT: 'c_value_texts',
        ValueTypeEnum.DATETIME: 'c_value_datetime',
        ValueTypeEnum.DATE: 'c_value_datetime',
        ValueTypeEnum.TIME: 'c_value_texts',
        ValueTypeEnum.FLOAT: 'c_value_floats',
        'index_{0}'.format(ValueTypeEnum.INT): 'c_value_index_integers',
        'index_{0}'.format(ValueTypeEnum.TEXT): 'c_value_index_texts',
        'index_{0}'.format(ValueTypeEnum.DATETIME): 'c_value_index_datetime',
        'index_{0}'.format(ValueTypeEnum.DATE): 'c_value_index_datetime',
        'index_{0}'.format(ValueTypeEnum.TIME): 'c_value_index_texts',
        'index_{0}'.format(ValueTypeEnum.FLOAT): 'c_value_index_floats',
    }

    es_type = {
        ValueTypeEnum.INT: 'long',
        ValueTypeEnum.TEXT: 'text',
        ValueTypeEnum.DATETIME: 'text',
        ValueTypeEnum.DATE: 'text',
        ValueTypeEnum.TIME: 'text',
        ValueTypeEnum.FLOAT: 'float'
    }


class TableMap(object):
    def __init__(self, attr_name=None):
        self.attr_name = attr_name

    @property
    def table(self):
        attr = AttributeCache.get(self.attr_name)
        i = "index_{0}".format(attr.value_type) if attr.is_index else attr.value_type
        return ValueTypeMap.table.get(i)

    @property
    def table_name(self):
        attr = AttributeCache.get(self.attr_name)
        i = "index_{0}".format(attr.value_type) if attr.is_index else attr.value_type
        return ValueTypeMap.table_name.get(i)
