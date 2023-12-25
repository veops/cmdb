# -*- coding:utf-8 -*-

import json
import re

from celery_once import QueueOnce
from flask import current_app
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound

from api.extensions import celery
from api.lib.decorator import flush_db
from api.lib.decorator import reconnect_db
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.audit import AuditOperateSource
from api.lib.perm.acl.audit import AuditOperateType
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import RoleRelationCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.record import OperateRecordCRUD
from api.models.acl import Resource
from api.models.acl import Role
from api.models.acl import Trigger


@celery.task(name="acl.role_rebuild",
             queue=ACL_QUEUE,)
@flush_db
@reconnect_db
def role_rebuild(rids, app_id):
    rids = rids if isinstance(rids, list) else [rids]
    for rid in rids:
        RoleRelationCache.rebuild(rid, app_id)

    current_app.logger.info("Role {0} App {1} rebuild..........".format(rids, app_id))


@celery.task(name="acl.update_resource_to_build_role", queue=ACL_QUEUE)
@reconnect_db
def update_resource_to_build_role(resource_id, app_id, group_id=None):
    rids = [i.id for i in Role.get_by(__func_isnot__key_uid=None, fl='id', to_dict=False)]
    rids += [i.id for i in Role.get_by(app_id=app_id, fl='id', to_dict=False)]
    rids += [i.id for i in Role.get_by(__func_is___key_uid=None, __func_is___key_app_id=None, fl='id', to_dict=False)]

    current_app.logger.info(rids)
    for rid in rids:
        if resource_id and resource_id in RoleRelationCache.get_resources(rid, app_id).get('id2perms', {}):
            RoleRelationCache.rebuild2(rid, app_id)

        if group_id and group_id in RoleRelationCache.get_resources(rid, app_id).get('group2perms', {}):
            RoleRelationCache.rebuild2(rid, app_id)


@celery.task(name="acl.apply_trigger", queue=ACL_QUEUE)
@flush_db
@reconnect_db
def apply_trigger(_id, resource_id=None, operator_uid=None):
    from api.lib.perm.acl.permission import PermissionCRUD

    trigger = Trigger.get_by_id(_id)
    if trigger is None:
        return

    uid = json.loads(trigger.uid or '[]')
    if resource_id is None:
        wildcard = (trigger.wildcard or '')

        if wildcard and uid:
            query = Resource.get_by(__func_in___key_uid=uid,
                                    app_id=trigger.app_id,
                                    resource_type_id=trigger.resource_type_id,
                                    fl=['id', 'app_id'],
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif wildcard:
            query = Resource.get_by(app_id=trigger.app_id,
                                    resource_type_id=trigger.resource_type_id,
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif uid:
            resources = Resource.get_by(__func_in___key_uid=uid,
                                        app_id=trigger.app_id,
                                        resource_type_id=trigger.resource_type_id,
                                        to_dict=False)
        else:
            resources = []
    else:
        resources = [Resource.get_by_id(resource_id)]

    perms = json.loads(trigger.permissions)
    roles = json.loads(trigger.roles)
    for resource in resources:
        for rid in roles:
            try:
                PermissionCRUD.grant(rid, perms, resource.id, rebuild=False, source=AuditOperateSource.trigger)
            except (NotFound, BadRequest):
                pass

    AuditCRUD.add_trigger_log(trigger.app_id, trigger.id, AuditOperateType.trigger_apply, {}, trigger.to_dict(),
                              {'uid': uid,
                               'resource_ids': [r.id for r in resources],
                               'perms': perms,
                               'rids': roles},
                              uid=operator_uid, source=AuditOperateSource.trigger)

    if resources:
        role_rebuild(roles, resources[0].app_id)


@celery.task(name="acl.cancel_trigger", queue=ACL_QUEUE)
@flush_db
@reconnect_db
def cancel_trigger(_id, resource_id=None, operator_uid=None):
    from api.lib.perm.acl.permission import PermissionCRUD

    trigger = Trigger.get_by_id(_id)
    if trigger is None:
        return

    uid = json.loads(trigger.uid or '[]')
    if resource_id is None:
        wildcard = (trigger.wildcard or '')

        if wildcard and uid:
            query = Resource.get_by(__func_in___key_uid=uid,
                                    app_id=trigger.app_id,
                                    resource_type_id=trigger.resource_type_id,
                                    fl=['id', 'app_id'],
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif wildcard:
            query = Resource.get_by(app_id=trigger.app_id,
                                    resource_type_id=trigger.resource_type_id,
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif uid:
            resources = Resource.get_by(__func_in___key_uid=uid,
                                        app_id=trigger.app_id,
                                        resource_type_id=trigger.resource_type_id,
                                        to_dict=False)
        else:
            resources = []
    else:
        resources = [Resource.get_by_id(resource_id)]

    perms = json.loads(trigger.permissions)
    roles = json.loads(trigger.roles)
    for resource in resources:
        if not resource:
            continue
        for rid in roles:
            try:
                PermissionCRUD.revoke(rid, perms, resource.id, rebuild=False, source=AuditOperateSource.trigger)
            except (NotFound, BadRequest):
                pass

    AuditCRUD.add_trigger_log(trigger.app_id, trigger.id, AuditOperateType.trigger_cancel, {}, trigger.to_dict(),
                              {'uid': uid,
                               'resource_ids': [r.id for r in resources if r],
                               'perms': perms,
                               'rids': roles},
                              uid=operator_uid, source=AuditOperateSource.trigger)

    if resources:
        role_rebuild(roles, resources[0].app_id)


@celery.task(name="acl.op_record", queue=ACL_QUEUE)
@reconnect_db
def op_record(app, role_name, operate_type, obj):
    if isinstance(app, int):
        app = AppCache.get(app)
        app = app and app.name

    if isinstance(role_name, int):
        u = UserCache.get(role_name)
        if u:
            role_name = u.username
        if not u:
            r = RoleCache.get(role_name)
            if r:
                role_name = r.name

    OperateRecordCRUD.add(app, role_name, operate_type, obj)
