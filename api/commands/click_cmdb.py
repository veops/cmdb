# -*- coding:utf-8 -*-


import json

import click
from flask.cli import with_appcontext

import api.lib.cmdb.ci
from api.extensions import rd
from api.models.cmdb import CI


@click.command()
@with_appcontext
def init_cache():
    cis = CI.get_by(to_dict=False)
    for ci in cis:
        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci.id, need_children=False, use_master=False)
        if rd.get([ci.id]):
            return
        rd.delete(ci.id)
        rd.add({ci.id: json.dumps(ci_dict)})
