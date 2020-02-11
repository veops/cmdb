# -*- coding: utf-8 -*-
"""provide some sample data in database"""
import uuid
import random

from api.models.cmdb import Attribute, CIType, CITypeAttributeGroup, CITypeAttribute


def init_attributes(num=1):
    attrs = []
    for i in range(num):
        attrs.append(Attribute.create(
            name=uuid.uuid4().hex[:8],
            alias=uuid.uuid4().hex[:8],
            value_type=str(random.randint(0, 100) % 7)
        ))
    return attrs


def init_ci_types(num=1):
    attrs = init_attributes(num)

    ci_types = []
    for i in range(num):
        ci_type = CIType.create(
            name=uuid.uuid4().hex[:8],
            alias=uuid.uuid4().hex[:8],
            unique_id=attrs[i].id
        )
        CITypeAttribute.create(
            type_id=ci_type.id,
            attr_id=attrs[i].id,
        )
        ci_types.append(ci_type)

    return ci_types


def init_attribute_groups(num=1):
    ci_types = init_ci_types(num)

    ags = []
    for i in range(num):
        ags.append(CITypeAttributeGroup.create(
            name=uuid.uuid4().hex[:8],
            type_id=ci_types[i].id,
            order=i
        ))
    return ags
