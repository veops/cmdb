# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import datetime
import json
import re

import six

import api.models.cmdb as model
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.const import ValueTypeEnum

TIME_RE = re.compile(r"^20|21|22|23|[0-1]\d:[0-5]\d:[0-5]\d$")


def string2int(x):
    return int(float(x))


def str2datetime(x):
    try:
        return datetime.datetime.strptime(x, "%Y-%m-%d").date()
    except ValueError:
        pass

    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


class ValueTypeMap(object):
    deserialize = {
        ValueTypeEnum.INT: string2int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: x,
        ValueTypeEnum.TIME: lambda x: TIME_RE.findall(x)[0],
        ValueTypeEnum.DATETIME: str2datetime,
        ValueTypeEnum.DATE: str2datetime,
        ValueTypeEnum.JSON: lambda x: json.loads(x) if isinstance(x, six.string_types) and x else x,
        ValueTypeEnum.PASSWORD: lambda x: x,
        ValueTypeEnum.LINK: lambda x: x,
    }

    serialize = {
        ValueTypeEnum.INT: int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: x if isinstance(x, six.string_types) else str(x),
        ValueTypeEnum.TIME: lambda x: x if isinstance(x, six.string_types) else str(x),
        ValueTypeEnum.DATE: lambda x: x.strftime("%Y-%m-%d") if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.DATETIME: lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.JSON: lambda x: json.loads(x) if isinstance(x, six.string_types) and x else x,
        ValueTypeEnum.PASSWORD: lambda x: x if isinstance(x, six.string_types) else str(x),
        ValueTypeEnum.LINK: lambda x: x if isinstance(x, six.string_types) else str(x),
    }

    serialize2 = {
        ValueTypeEnum.INT: int,
        ValueTypeEnum.FLOAT: float,
        ValueTypeEnum.TEXT: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.TIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.DATE: lambda x: (x.decode() if not isinstance(x, six.string_types) else x).split()[0],
        ValueTypeEnum.DATETIME: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.JSON: lambda x: json.loads(x) if isinstance(x, six.string_types) and x else x,
        ValueTypeEnum.PASSWORD: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
        ValueTypeEnum.LINK: lambda x: x.decode() if not isinstance(x, six.string_types) else x,
    }

    choice = {
        ValueTypeEnum.INT: model.IntegerChoice,
        ValueTypeEnum.FLOAT: model.FloatChoice,
        ValueTypeEnum.TEXT: model.TextChoice,
        ValueTypeEnum.TIME: model.TextChoice,
        ValueTypeEnum.DATE: model.TextChoice,
        ValueTypeEnum.DATETIME: model.TextChoice,
    }

    table = {
        ValueTypeEnum.TEXT: model.CIValueText,
        ValueTypeEnum.JSON: model.CIValueJson,
        ValueTypeEnum.PASSWORD: model.CIValueText,
        ValueTypeEnum.LINK: model.CIValueText,
        'index_{0}'.format(ValueTypeEnum.INT): model.CIIndexValueInteger,
        'index_{0}'.format(ValueTypeEnum.TEXT): model.CIIndexValueText,
        'index_{0}'.format(ValueTypeEnum.DATETIME): model.CIIndexValueDateTime,
        'index_{0}'.format(ValueTypeEnum.DATE): model.CIIndexValueDateTime,
        'index_{0}'.format(ValueTypeEnum.TIME): model.CIIndexValueText,
        'index_{0}'.format(ValueTypeEnum.FLOAT): model.CIIndexValueFloat,
        'index_{0}'.format(ValueTypeEnum.JSON): model.CIValueJson,
    }

    table_name = {
        ValueTypeEnum.TEXT: 'c_value_texts',
        ValueTypeEnum.JSON: 'c_value_json',
        ValueTypeEnum.PASSWORD: 'c_value_texts',
        ValueTypeEnum.LINK: 'c_value_texts',
        'index_{0}'.format(ValueTypeEnum.INT): 'c_value_index_integers',
        'index_{0}'.format(ValueTypeEnum.TEXT): 'c_value_index_texts',
        'index_{0}'.format(ValueTypeEnum.DATETIME): 'c_value_index_datetime',
        'index_{0}'.format(ValueTypeEnum.DATE): 'c_value_index_datetime',
        'index_{0}'.format(ValueTypeEnum.TIME): 'c_value_index_texts',
        'index_{0}'.format(ValueTypeEnum.FLOAT): 'c_value_index_floats',
        'index_{0}'.format(ValueTypeEnum.JSON): 'c_value_json',
    }

    es_type = {
        ValueTypeEnum.INT: 'long',
        ValueTypeEnum.TEXT: 'text',
        ValueTypeEnum.DATETIME: 'text',
        ValueTypeEnum.DATE: 'text',
        ValueTypeEnum.TIME: 'text',
        ValueTypeEnum.FLOAT: 'float',
        ValueTypeEnum.JSON: 'object',
        ValueTypeEnum.PASSWORD: 'text',
        ValueTypeEnum.LINK: 'text',
    }


class TableMap(object):
    def __init__(self, attr_name=None, attr=None, is_index=None):
        self.attr_name = attr_name
        self.attr = attr
        self.is_index = is_index

    @property
    def table(self):
        attr = AttributeCache.get(self.attr_name) if not self.attr else self.attr
        if attr.value_type not in {ValueTypeEnum.TEXT, ValueTypeEnum.JSON, ValueTypeEnum.PASSWORD, ValueTypeEnum.LINK}:
            self.is_index = True
        elif self.is_index is None:
            self.is_index = attr.is_index

        i = "index_{0}".format(attr.value_type) if self.is_index else attr.value_type

        return ValueTypeMap.table.get(i)

    @property
    def table_name(self):
        attr = AttributeCache.get(self.attr_name) if not self.attr else self.attr
        if attr.value_type not in {ValueTypeEnum.TEXT, ValueTypeEnum.JSON, ValueTypeEnum.PASSWORD, ValueTypeEnum.LINK}:
            self.is_index = True
        elif self.is_index is None:
            self.is_index = attr.is_index

        i = "index_{0}".format(attr.value_type) if self.is_index else attr.value_type

        return ValueTypeMap.table_name.get(i)
