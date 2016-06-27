# -*- coding:utf-8 -*- 


import datetime

from markupsafe import escape

from models.attribute import TextChoice
from models.attribute import FloatChoice
from models.attribute import IntegerChoice
from models.attribute import CIAttributeCache
from models.ci_value import CIValueText
from models.ci_value import CIValueInteger
from models.ci_value import CIValueFloat
from models.ci_value import CIValueDateTime
from models.ci_value import CIIndexValueDateTime
from models.ci_value import CIIndexValueFloat
from models.ci_value import CIIndexValueInteger
from models.ci_value import CIIndexValueText


def string2int(x):
    return int(float(x))


def str2datetime(x):
    try:
        v = datetime.datetime.strptime(x, "%Y-%m-%d")
        return v
    except ValueError:
        pass
    try:
        v = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        return v
    except ValueError:
        pass
    raise ValueError


type_map = {
    'converter': {
        'int': string2int,
        'float': float,
        'text': escape,
        'datetime': str2datetime,
    },
    'choice': {
        'int': IntegerChoice,
        'float': FloatChoice,
        'text': TextChoice,
    },
    'table': {
        'int': CIValueInteger,
        'text': CIValueText,
        'datetime': CIValueDateTime,
        'float': CIValueFloat,
        'index_int': CIIndexValueInteger,
        'index_text': CIIndexValueText,
        'index_datetime': CIIndexValueDateTime,
        'index_float': CIIndexValueFloat,
    },
    'table_name': {
        'int': 'integers',
        'text': 'texts',
        'datetime': 'datetime',
        'float': 'floats',
        'index_int': 'index_integers',
        'index_text': 'index_texts',
        'index_datetime': 'index_datetime',
        'index_float': 'index_floats',
    }
}


class TableMap():
    def __init__(self, attr_name=None):
        self.attr_name = attr_name

    @property
    def table(self):
        if self.attr_name is not None:
            attr = CIAttributeCache.get(self.attr_name)
            if attr.is_index:
                i = "index_{0}".format(attr.value_type)
            else:
                i = attr.value_type
            return type_map["table"].get(i)

    @property
    def table_name(self):
        if self.attr_name is not None:
            attr = CIAttributeCache.get(self.attr_name)
            if attr.is_index:
                i = "index_{0}".format(attr.value_type)
            else:
                i = attr.value_type
            return type_map["table_name"].get(i)


CITYPE_RELATION_TYPES = ["connect", "deploy", "install", "contain"]
CI_RELATION_TYPES = ["connect", "deploy", "install", "contain"]