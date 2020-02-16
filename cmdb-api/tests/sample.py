# -*- coding: utf-8 -*-
"""provide some sample data in database"""
import uuid
import random

from api.models.cmdb import (
    Attribute,
    CIType,
    CITypeAttributeGroup,
    CITypeAttribute,
    CITypeRelation,
    RelationType
)


def init_attributes(num=1):
    attrs = []
    for i in range(num):
        attrs.append(Attribute.create(
            name=uuid.uuid4().hex[:8],
            alias=uuid.uuid4().hex[:8],
            value_type=str(random.randint(0, 100) % 3)
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


def init_relation_type(num=1):
    result = []
    for i in range(num):
        result.append(RelationType.create(
            name=uuid.uuid4().hex[:8],
        ))
    return result


def init_ci_type_relation(num=1):
    result = []
    ci_types = init_ci_types(num+1)
    relation_types = init_relation_type(num)
    for i in range(num):
        result.append(CITypeRelation.create(
            parent_id=ci_types[i].id,
            child_id=ci_types[i+1].id,
            relation_type_id=relation_types[i].id
        ))
    return result


def fake_attr_value(attr_dict):
    attr_type = attr_dict["value_type"]
    attr_name = attr_dict["name"]

    if attr_type == "0":
        return {attr_name: random.randint(0, 1000)}
    elif attr_type == "1":
        return {attr_name: random.randint(0, 1000) / 3.0}
    elif attr_type == "2":
        return {attr_name: uuid.uuid4().hex[:8]}
