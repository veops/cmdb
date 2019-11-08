# -*- coding:utf-8 -*-

from flask import current_app

from api.extensions import celery
from api.lib.perm.acl.cache import RoleRelationCache
from api.lib.perm.acl.const import ACL_QUEUE


@celery.task(name="acl.role_rebuild", queue=ACL_QUEUE)
def role_rebuild(rids):
    rids = rids if isinstance(rids, list) else [rids]
    for rid in rids:
        RoleRelationCache.rebuild(rid)

    current_app.logger.info("%d rebuild.........." % rids)
