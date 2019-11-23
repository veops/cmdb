# -*- coding:utf-8 -*-


import json

import click
from flask import current_app
from flask.cli import with_appcontext

import api.lib.cmdb.ci
from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.cmdb.const import ValueTypeEnum
from api.models.cmdb import CI
from api.models.cmdb import CIRelation


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
        relations.setdefault(cr.first_ci_id, []).append(cr.second_ci_id)
    for i in relations:
        relations[i] = json.dumps(relations[i])
    if relations:
        rd.create_or_update(relations, REDIS_PREFIX_CI_RELATION)

    db.session.remove()
