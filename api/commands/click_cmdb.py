# -*- coding:utf-8 -*-


import json

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import BadRequest

import api.lib.cmdb.ci
from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.const import ValueTypeEnum
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resource import ResourceTypeCRUD
from api.lib.perm.acl.role import RoleCRUD
from api.models.acl import ResourceType
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CIType
from api.models.cmdb import PreferenceRelationView


@click.command()
@with_appcontext
def init_cache():
    db.session.remove()

    if current_app.config.get("USE_ES"):
        from api.extensions import es
        from api.models.cmdb import Attribute
        from api.lib.cmdb.utils import ValueTypeMap
        attributes = Attribute.get_by(to_dict=False)
        for attr in attributes:
            other = dict()
            other['index'] = True if attr.is_index else False
            if attr.value_type == ValueTypeEnum.TEXT:
                other['analyzer'] = 'ik_max_word'
                other['search_analyzer'] = 'ik_smart'
                if attr.is_index:
                    other["fields"] = {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
            try:
                es.update_mapping(attr.name, ValueTypeMap.es_type[attr.value_type], other)
            except Exception as e:
                print(e)

    cis = CI.get_by(to_dict=False)
    for ci in cis:
        if current_app.config.get("USE_ES"):
            res = es.get_index_id(ci.id)
            if res:
                continue
        else:
            res = rd.get([ci.id], REDIS_PREFIX_CI)
            if res and list(filter(lambda x: x, res)):
                continue

        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci.id, need_children=False, use_master=False)

        if current_app.config.get("USE_ES"):
            es.create(ci_dict)
        else:
            rd.create_or_update({ci.id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

    ci_relations = CIRelation.get_by(to_dict=False)
    relations = dict()
    for cr in ci_relations:
        relations.setdefault(cr.first_ci_id, {}).update({cr.second_ci_id: cr.second_ci.type_id})
    for i in relations:
        relations[i] = json.dumps(relations[i])
    if relations:
        rd.create_or_update(relations, REDIS_PREFIX_CI_RELATION)

    db.session.remove()


@click.command()
@with_appcontext
def init_acl():
    app_id = AppCache.get('cmdb').id
    # 1. add resource type
    for resource_type in ResourceTypeEnum.all():
        try:
            ResourceTypeCRUD.add(app_id, resource_type, '', PermEnum.all())
        except BadRequest:
            pass

    # 2. add role
    try:
        RoleCRUD.add_role(RoleEnum.CONFIG, app_id, True)
    except BadRequest:
        pass
    try:
        RoleCRUD.add_role(RoleEnum.CMDB_READ_ALL, app_id, False)
    except BadRequest:
        pass

    # 3. add resource and grant
    ci_types = CIType.get_by(to_dict=False)
    type_id = ResourceType.get_by(name=ResourceTypeEnum.CI, first=True, to_dict=False).id
    for ci_type in ci_types:
        try:
            ResourceCRUD.add(ci_type.name, type_id, app_id)
        except BadRequest:
            pass

        ACLManager().grant_resource_to_role(ci_type.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.CI,
                                            [PermEnum.READ])

    relation_views = PreferenceRelationView.get_by(to_dict=False)
    type_id = ResourceType.get_by(name=ResourceTypeEnum.RELATION_VIEW, first=True, to_dict=False).id
    for view in relation_views:
        try:
            ResourceCRUD.add(view.name, type_id, app_id)
        except BadRequest:
            pass

        ACLManager().grant_resource_to_role(view.name,
                                            RoleEnum.CMDB_READ_ALL,
                                            ResourceTypeEnum.RELATION_VIEW,
                                            [PermEnum.READ])
