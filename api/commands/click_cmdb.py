# -*- coding:utf-8 -*-


import json

import click
from flask import current_app
from flask.cli import with_appcontext

import api.lib.cmdb.ci
from api.extensions import db
from api.extensions import es
from api.extensions import rd
from api.models.cmdb import CI


@click.command()
@with_appcontext
def init_cache():
    db.session.remove()

    cis = CI.get_by(to_dict=False)
    for ci in cis:
        if current_app.config.get("USE_ES"):
            res = es.get_index_id(ci.id)
            if res:
                continue
        else:
            res = rd.get([ci.id])
            if res and list(filter(lambda x: x, res)):
                continue

        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci.id, need_children=False, use_master=False)

        if current_app.config.get("USE_ES"):
            es.create(ci_dict)
        else:
            rd.delete(ci.id)
            rd.add({ci.id: json.dumps(ci_dict)})

    db.session.remove()
