# -*- coding:utf-8 -*-


import copy
import json
import re
from fnmatch import fnmatch

from flask import abort

from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.audit import AuditOperateType
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.resp_format import ErrFormat
from api.models.acl import Trigger
from api.tasks.acl import apply_trigger, cancel_trigger


class TriggerCRUD(object):
    cls = Trigger

    @staticmethod
    def get(app_id):
        triggers = Trigger.get_by(app_id=app_id)
        for trigger in triggers:
            trigger['uid'] = json.loads(trigger['uid'] or '[]')
            trigger['users'] = [UserCache.get(i).username for i in trigger['uid']]
            trigger['roles'] = json.loads(trigger['roles'] or '[]')
            trigger['permissions'] = json.loads(trigger['permissions'] or '[]')

        return triggers

    @staticmethod
    def add(app_id, **kwargs):
        kwargs.pop('app_id', None)
        kwargs['roles'] = json.dumps(kwargs['roles'] or [])
        kwargs['permissions'] = json.dumps(kwargs['permissions'] or [])

        kwargs['uid'] = json.dumps(kwargs.get('uid') or [])

        _kwargs = copy.deepcopy(kwargs)
        _kwargs.pop('name', None)

        Trigger.get_by(app_id=app_id, **_kwargs) and abort(400, ErrFormat.trigger_exists.format(""))
        t = Trigger.create(app_id=app_id, **kwargs)

        AuditCRUD.add_trigger_log(app_id, t.id, AuditOperateType.create, {}, t.to_dict(), {})

        return t

    @staticmethod
    def update(_id, **kwargs):
        existed = Trigger.get_by_id(_id) or abort(404, ErrFormat.trigger_not_found.format("id={}".format(_id)))
        origin = existed.to_dict()
        kwargs['roles'] = json.dumps(kwargs['roles'] or [])
        kwargs['uid'] = json.dumps(kwargs['uid'] or [])
        kwargs['permissions'] = json.dumps(kwargs['permissions'] or [])

        existed.update(**kwargs)

        AuditCRUD.add_trigger_log(existed.app_id, existed.id, AuditOperateType.update,
                                  origin, existed.to_dict(), {})

        return existed

    @staticmethod
    def delete(_id):
        existed = Trigger.get_by_id(_id) or abort(404, ErrFormat.trigger_not_found.format("id={}".format(_id)))
        origin = existed.to_dict()

        existed.soft_delete()

        AuditCRUD.add_trigger_log(existed.app_id, existed.id, AuditOperateType.delete,
                                  origin, {}, {}
                                  )

        return existed

    @staticmethod
    def apply(_id):
        trigger = Trigger.get_by_id(_id) or abort(404, ErrFormat.trigger_not_found.format("id={}".format(_id)))
        if not trigger.enabled:
            return abort(400, ErrFormat.trigger_disabled.format("id={}".format(_id)))

        user_id = AuditCRUD.get_current_operate_uid()

        apply_trigger.apply_async(args=(_id,), kwargs=dict(operator_uid=user_id), queue=ACL_QUEUE)

    @staticmethod
    def cancel(_id):
        trigger = Trigger.get_by_id(_id) or abort(404, ErrFormat.trigger_not_found.format("id={}".format(_id)))
        if not trigger.enabled:
            return abort(400, ErrFormat.trigger_disabled.format("id={}".format(_id)))

        user_id = AuditCRUD.get_current_operate_uid()

        cancel_trigger.apply_async(args=(_id,), kwargs=dict(operator_uid=user_id), queue=ACL_QUEUE)

    @staticmethod
    def match_triggers(app_id, resource_name, resource_type_id, uid):
        triggers = Trigger.get_by(app_id=app_id, enabled=True, resource_type_id=resource_type_id, to_dict=False)

        def _fnmatch(name, wildcard):
            import re

            try:
                return re.compile(wildcard).findall(name)
            except:
                return fnmatch(name, trigger.wildcard)

        uid = int(uid) if uid else uid
        _match_triggers = []
        for trigger in triggers:
            uids = json.loads(trigger.uid or '[]')
            if trigger.wildcard and uids:
                if _fnmatch(resource_name, trigger.wildcard) and uid in uids:
                    _match_triggers.append(trigger)
            elif trigger.wildcard:
                if _fnmatch(resource_name, trigger.wildcard):
                    _match_triggers.append(trigger)
            elif uids:
                if uid in uids:
                    _match_triggers.append(trigger)

        return _match_triggers

    @staticmethod
    def get_resources(app_id, resource_type_id, wildcard, uid):
        from api.models.acl import Resource

        wildcard = wildcard or ''

        if wildcard and uid:
            query = Resource.get_by(__func_in___key_uid=uid,
                                    app_id=app_id,
                                    resource_type_id=resource_type_id,
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif wildcard:
            query = Resource.get_by(app_id=app_id,
                                    resource_type_id=resource_type_id,
                                    only_query=True)
            try:
                re.compile(wildcard)

                resources = query.filter(Resource.name.op('regexp')(wildcard)).all()
            except:
                resources = query.filter(Resource.name.ilike(wildcard.replace('*', '%'))).all()
        elif uid:
            resources = Resource.get_by(__func_in___key_uid=uid,
                                        app_id=app_id,
                                        resource_type_id=resource_type_id,
                                        to_dict=False)
        else:
            resources = []

        return resources
