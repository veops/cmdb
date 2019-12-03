# -*- coding:utf-8 -*- 


import json
import time

from flask import current_app

import api.lib.cmdb.ci
from api.extensions import celery
from api.extensions import db
from api.extensions import es
from api.extensions import rd
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.models.cmdb import CIRelation


@celery.task(name="cmdb.ci_cache", queue=CMDB_QUEUE)
def ci_cache(ci_id):
    time.sleep(0.01)
    db.session.close()

    m = api.lib.cmdb.ci.CIManager()
    ci = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)
    if current_app.config.get("USE_ES"):
        es.create_or_update(ci_id, ci)
    else:
        rd.create_or_update({ci_id: json.dumps(ci)}, REDIS_PREFIX_CI)

    current_app.logger.info("{0} flush..........".format(ci_id))


@celery.task(name="cmdb.ci_delete", queue=CMDB_QUEUE)
def ci_delete(ci_id):
    current_app.logger.info(ci_id)

    if current_app.config.get("USE_ES"):
        es.delete(ci_id)
    else:
        rd.delete(ci_id, REDIS_PREFIX_CI)

    current_app.logger.info("{0} delete..........".format(ci_id))


@celery.task(name="cmdb.ci_relation_cache", queue=CMDB_QUEUE)
def ci_relation_cache(parent_id, child_id):
    children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
    children = json.loads(children) if children is not None else {}

    cr = CIRelation.get_by(first_ci_id=parent_id, second_ci_id=child_id, first=True, to_dict=False)
    if child_id not in children:
        children[child_id] = cr.second_ci.type_id

    rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

    current_app.logger.info("ADD ci relation cache: {0} -> {1}".format(parent_id, child_id))


@celery.task(name="cmdb.ci_relation_delete", queue=CMDB_QUEUE)
def ci_relation_delete(parent_id, child_id):
    children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
    children = json.loads(children) if children is not None else {}

    if child_id in children:
        children.pop(child_id)

    rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

    current_app.logger.info("DELETE ci relation cache: {0} -> {1}".format(parent_id, child_id))
