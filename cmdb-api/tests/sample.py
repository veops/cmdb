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
from api.models.acl import User

from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci import CIManager, CIRelationManager


def force_add_user():
    from flask import g
    if not getattr(g, "user", None):
        g.user = User.query.first()


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


def init_ci(num=1):
    # store ci need has user
    force_add_user()
    ci_type = init_ci_types(1)[0]
    attrs = CITypeAttributeManager.get_attributes_by_type_id(ci_type.id)
    manager = CIManager()
    result = []

    for i in range(num):
        ci_id = manager.add(ci_type.name, **fake_attr_value(attrs[0]))
        result.append(manager.get_ci_by_id_from_db(ci_id))

    return result


def init_ci_with_type(ci_types):
    force_add_user()
    cis = []
    manager = CIManager()
    for ci_type in ci_types:
        attrs = CITypeAttributeManager.get_attributes_by_type_id(ci_type.id)
        ci_id = manager.add(ci_type.name, **fake_attr_value(attrs[0]))
        cis.append(manager.get_ci_by_id_from_db(ci_id))
    return cis


def init_ci_relation():
    init_ci_type_relation(1)
    ci_types = CIType.query.all()
    cis = init_ci_with_type(ci_types)
    manager = CIRelationManager()
    cir_id = manager.add(cis[0]['ci_id'], cis[1]['ci_id'])
    return cir_id
