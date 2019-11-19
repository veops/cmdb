# -*- coding:utf-8 -*- 


import json
import time

from flask import current_app

import api.lib.cmdb.ci
from api.extensions import celery
from api.extensions import db
from api.extensions import rd
from api.extensions import es
from api.lib.cmdb.const import CMDB_QUEUE


@celery.task(name="cmdb.ci_cache", queue=CMDB_QUEUE)
def ci_cache(ci_id):
    time.sleep(0.1)
    db.session.close()

    m = api.lib.cmdb.ci.CIManager()
    ci = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)
    if current_app.config.get("USE_ES"):
        es.update(ci_id, ci)
    else:
        rd.delete(ci_id)
        rd.add({ci_id: json.dumps(ci)})

    current_app.logger.info("%d flush.........." % ci_id)


@celery.task(name="cmdb.ci_delete", queue=CMDB_QUEUE)
def ci_delete(ci_id):
    current_app.logger.info(ci_id)

    if current_app.config.get("USE_ES"):
        es.delete(ci_id)
    else:
        rd.delete(ci_id)

    current_app.logger.info("%d delete.........." % ci_id)
