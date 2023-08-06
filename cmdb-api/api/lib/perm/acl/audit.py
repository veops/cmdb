# -*- coding:utf-8 -*-
import itertools
import json
from enum import Enum
from typing import List

from flask import g, has_request_context, request
from flask_login import current_user
from sqlalchemy import func

from api.lib.perm.acl import AppCache
from api.models.acl import AuditPermissionLog, AuditResourceLog, AuditRoleLog, AuditTriggerLog, Permission, Resource, \
    ResourceGroup, ResourceType, Role, RolePermission


class AuditScope(str, Enum):
    app = 'app'
    resource = 'resource'
    resource_type = 'resource_type'
    resource_group = 'resource_group'

    user = 'user'
    role = 'role'
    role_relation = 'role_relation'


class AuditOperateType(str, Enum):
    read = 'read'
    create = 'create'
    update = 'update'
    delete = 'delete'

    user_login = 'user_login'
    role_relation_add = 'role_relation_add'
    role_relation_delete = 'role_relation_delete'
    grant = 'grant'
    revoke = 'revoke'
    trigger_apply = 'trigger_apply'
    trigger_cancel = 'trigger_cancel'


class AuditOperateSource(str, Enum):
    api = 'api'
    acl = 'acl'
    trigger = 'trigger'


class AuditCRUD(object):

    @staticmethod
    def get_current_operate_uid(uid=None):

        user_id = uid or (hasattr(g, 'user') and getattr(current_user, 'uid', None)) \
                  or getattr(current_user, 'user_id', None)

        if has_request_context() and request.headers.get('X-User-Id'):
            _user_id = request.headers['X-User-Id']
            user_id = int(_user_id) if _user_id.isdigit() else uid

        return user_id

    @staticmethod
    def get_operate_source(source):
        if has_request_context() and request.headers.get('App-Access-Token'):
            source = AuditOperateSource.api

        return source

    @staticmethod
    def search_permission(app_id, q=None, page=1, page_size=10, start=None, end=None):
        criterion = []
        if app_id:
            app = AppCache.get(app_id)
            criterion.append(AuditPermissionLog.app_id == app.id)

        if start:
            criterion.append(AuditPermissionLog.created_at >= start)
        if end:
            criterion.append(AuditPermissionLog.created_at <= end)

        kwargs = {expr.split(':')[0]: expr.split(':')[1] for expr in q.split(',')} if q else {}
        for k, v in kwargs.items():
            if k == 'resource_type_id':
                criterion.append(AuditPermissionLog.resource_type_id == int(v))
            elif k == 'rid':
                criterion.append(AuditPermissionLog.rid == int(v))
            elif k == 'resource_id':
                criterion.append(func.json_contains(AuditPermissionLog.resource_ids, v) == 1)

            elif k == 'operate_uid':
                criterion.append(AuditPermissionLog.operate_uid == v)
            elif k == 'operate_type':
                criterion.append(AuditPermissionLog.operate_type == v)

        records = AuditPermissionLog.query.filter(
            AuditPermissionLog.deleted == 0,
            *criterion) \
            .order_by(AuditPermissionLog.id.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size).all()

        data = {
            'data': [r.to_dict() for r in records],
            'id2resources': {},
            'id2roles': {},
            'id2groups': {},
            'id2perms': {},
            'id2resource_types': {},
        }

        resource_ids = set(itertools.chain(*[r.resource_ids for r in records]))
        group_ids = set(itertools.chain(*[r.group_ids for r in records]))
        permission_ids = set(itertools.chain(*[r.permission_ids for r in records]))
        resource_type_ids = {r.resource_type_id for r in records}
        rids = {r.rid for r in records}

        if rids:
            roles = Role.query.filter(Role.id.in_(rids)).all()
            data['id2roles'] = {r.id: r.to_dict() for r in roles}

        if resource_type_ids:
            resource_types = ResourceType.query.filter(ResourceType.id.in_(resource_type_ids)).all()
            data['id2resource_types'] = {r.id: r.to_dict() for r in resource_types}

        if resource_ids:
            resources = Resource.query.filter(Resource.id.in_(resource_ids)).all()
            data['id2resources'] = {r.id: r.to_dict() for r in resources}

        if group_ids:
            groups = ResourceGroup.query.filter(ResourceGroup.id.in_(group_ids)).all()
            data['id2groups'] = {_g.id: _g.to_dict() for _g in groups}

        if permission_ids:
            perms = Permission.query.filter(Permission.id.in_(permission_ids)).all()

            data['id2perms'] = {_p.id: _p.to_dict() for _p in perms}

        return data

    @staticmethod
    def search_role(app_id, q=None, page=1, page_size=10, start=None, end=None):
        criterion = []
        if app_id:
            app = AppCache.get(app_id)
            criterion.append(AuditRoleLog.app_id == app.id)

        if start:
            criterion.append(AuditRoleLog.created_at >= start)
        if end:
            criterion.append(AuditRoleLog.created_at <= end)

        kwargs = {expr.split(':')[0]: expr.split(':')[1] for expr in q.split(',')} if q else {}
        for k, v in kwargs.items():
            if k == 'scope':
                criterion.append(AuditRoleLog.scope == v)
            elif k == 'link_id':
                criterion.append(AuditRoleLog.link_id == int(v))
            elif k == 'operate_uid':
                criterion.append(AuditRoleLog.operate_uid == v)
            elif k == 'operate_type':
                criterion.append(AuditRoleLog.operate_type == v)

        records = AuditRoleLog.query.filter(AuditRoleLog.deleted == 0, *criterion) \
            .order_by(AuditRoleLog.id.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size).all()

        data = {
            'data': [r.to_dict() for r in records],
            'id2roles': {}
        }

        role_permissions = list(itertools.chain(*[r.extra.get('role_permissions', []) for r in records]))
        _rids = set()
        if role_permissions:

            resource_ids = set([r['resource_id'] for r in role_permissions])
            group_ids = set([r['group_id'] for r in role_permissions])
            perm_ids = set([r['perm_id'] for r in role_permissions])
            _rids.update(set([r['rid'] for r in role_permissions]))

            if resource_ids:
                resources = Resource.query.filter(Resource.id.in_(resource_ids)).all()
                data['id2resources'] = {r.id: r.to_dict() for r in resources}

            if group_ids:
                groups = ResourceGroup.query.filter(ResourceGroup.id.in_(group_ids)).all()
                data['id2groups'] = {_g.id: _g.to_dict() for _g in groups}

            if perm_ids:
                perms = Permission.query.filter(Permission.id.in_(perm_ids)).all()

                data['id2perms'] = {_p.id: _p.to_dict() for _p in perms}

        rids = set(itertools.chain(*[r.extra.get('child_ids', []) + r.extra.get('parent_ids', [])
                                     for r in records]))
        rids.update(_rids)
        if rids:
            roles = Role.query.filter(Role.id.in_(rids)).all()
            data['id2roles'].update({r.id: r.to_dict() for r in roles})

        return data

    @staticmethod
    def search_resource(app_id, q=None, page=1, page_size=10, start=None, end=None):
        criterion = []
        if app_id:
            app = AppCache.get(app_id)
            criterion.append(AuditResourceLog.app_id == app.id)

        if start:
            criterion.append(AuditResourceLog.created_at >= start)
        if end:
            criterion.append(AuditResourceLog.created_at <= end)

        kwargs = {expr.split(':')[0]: expr.split(':')[1] for expr in q.split(',')} if q else {}
        for k, v in kwargs.items():
            if k == 'scope':
                criterion.append(AuditResourceLog.scope == v)
            elif k == 'link_id':
                criterion.append(AuditResourceLog.link_id == int(v))
            elif k == 'operate_uid':
                criterion.append(AuditResourceLog.operate_uid == v)
            elif k == 'operate_type':
                criterion.append(AuditResourceLog.operate_type == v)

        records = AuditResourceLog.query.filter(
            AuditResourceLog.deleted == 0,
            *criterion) \
            .order_by(AuditResourceLog.id.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size).all()

        data = {
            'data': [r.to_dict() for r in records],
        }

        return data

    @staticmethod
    def search_trigger(app_id, q=None, page=1, page_size=10, start=None, end=None):
        criterion = []
        if app_id:
            app = AppCache.get(app_id)
            criterion.append(AuditTriggerLog.app_id == app.id)

        if start:
            criterion.append(AuditTriggerLog.created_at >= start)
        if end:
            criterion.append(AuditTriggerLog.created_at <= end)

        kwargs = {expr.split(':')[0]: expr.split(':')[1] for expr in q.split(',')} if q else {}
        for k, v in kwargs.items():
            if k == 'trigger_id':
                criterion.append(AuditTriggerLog.trigger_id == int(v))
            elif k == 'operate_uid':
                criterion.append(AuditTriggerLog.operate_uid == v)
            elif k == 'operate_type':
                criterion.append(AuditTriggerLog.operate_type == v)

        records = AuditTriggerLog.query.filter(
            AuditTriggerLog.deleted == 0,
            *criterion) \
            .order_by(AuditTriggerLog.id.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size).all()

        data = {
            'data': [r.to_dict() for r in records],
            'id2roles': {},
            'id2resource_types': {},
        }

        rids = set(itertools.chain(*[json.loads(r.origin.get('roles', "[]")) +
                                     json.loads(r.current.get('roles', "[]"))
                                     for r in records]))
        resource_type_ids = set([r.origin.get('resource_type_id') for r in records
                                 if r.origin.get('resource_type_id')] +
                                [r.current.get('resource_type_id') for r in records
                                 if r.current.get('resource_type_id')])
        if rids:
            roles = Role.query.filter(Role.id.in_(rids)).all()
            data['id2roles'] = {r.id: r.to_dict() for r in roles}

        if resource_type_ids:
            resource_types = ResourceType.query.filter(ResourceType.id.in_(resource_type_ids)).all()
            data['id2resource_types'] = {r.id: r.to_dict() for r in resource_types}

        return data

    @classmethod
    def add_role_log(cls, app_id, operate_type: AuditOperateType,
                     scope: AuditScope, link_id: int, origin: dict, current: dict, extra: dict,
                     uid=None, source=AuditOperateSource.acl):

        user_id = cls.get_current_operate_uid(uid)

        AuditRoleLog.create(app_id=app_id, operate_uid=user_id, operate_type=operate_type.value,
                            scope=scope.value,
                            link_id=link_id,
                            origin=origin,
                            current=current,
                            extra=extra,
                            source=source.value)

    @classmethod
    def add_resource_log(cls, app_id, operate_type: AuditOperateType,
                         scope: AuditScope, link_id: int, origin: dict, current: dict, extra: dict,
                         uid=None, source=AuditOperateSource.acl):
        user_id = cls.get_current_operate_uid(uid)

        source = cls.get_operate_source(source)

        AuditResourceLog.create(app_id=app_id, operate_uid=user_id, operate_type=operate_type.value,
                                scope=scope.value,
                                link_id=link_id,
                                origin=origin,
                                current=current,
                                extra=extra,
                                source=source.value)

    @classmethod
    def add_permission_log(cls, app_id, operate_type: AuditOperateType,
                           rid: int, rt_id: int, role_permissions: List[RolePermission],
                           uid=None, source=AuditOperateSource.acl):

        if not role_permissions:
            return
        user_id = cls.get_current_operate_uid(uid)
        source = cls.get_operate_source(source)

        resource_ids = list({r.resource_id for r in role_permissions if r.resource_id})
        permission_ids = list({r.perm_id for r in role_permissions if r.perm_id})
        group_ids = list({r.group_id for r in role_permissions if r.group_id})

        AuditPermissionLog.create(app_id=app_id, operate_uid=user_id,
                                  operate_type=operate_type.value,
                                  rid=rid,
                                  resource_type_id=rt_id,
                                  resource_ids=resource_ids,
                                  permission_ids=permission_ids,
                                  group_ids=group_ids,
                                  source=source.value)

    @classmethod
    def add_trigger_log(cls, app_id, trigger_id, operate_type: AuditOperateType,
                        origin: dict, current: dict, extra: dict,
                        uid=None, source=AuditOperateSource.acl):

        user_id = cls.get_current_operate_uid(uid)
        source = cls.get_operate_source(source)

        AuditTriggerLog.create(app_id=app_id, trigger_id=trigger_id, operate_uid=user_id,
                               operate_type=operate_type.value,
                               origin=origin, current=current, extra=extra, source=source.value)
