# -*- coding:utf-8 -*-

import functools

from flask import abort
from flask import current_app
from flask import g
from flask import request

from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.mixin import DBMixin
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.models.cmdb import CIFilterPerms


class CIFilterPermsCRUD(DBMixin):
    cls = CIFilterPerms

    def get(self, type_id):
        res = self.cls.get_by(type_id=type_id, to_dict=True)
        result = {}
        for i in res:
            if i['attr_filter']:
                i['attr_filter'] = i['attr_filter'].split(',')

            if i['rid'] not in result:
                result[i['rid']] = i
            else:
                if i['attr_filter']:
                    if not result[i['rid']]['attr_filter']:
                        result[i['rid']]['attr_filter'] = []

                    result[i['rid']]['attr_filter'] += i['attr_filter']
                    result[i['rid']]['attr_filter'] = list(set(i['attr_filter']))
                if i['ci_filter']:
                    if not result[i['rid']]['ci_filter']:
                        result[i['rid']]['ci_filter'] = ""
                    result[i['rid']]['ci_filter'] += (i['ci_filter'] or "")

        return result

    def get_by_ids(self, _ids, type_id=None):
        if not _ids:
            return {}

        if type_id is not None:
            res = self.cls.get_by(type_id=type_id, __func_in___key_id=_ids, to_dict=True)
        else:
            res = self.cls.get_by(__func_in___key_id=_ids, to_dict=True)

        result = {}
        for i in res:
            if i['attr_filter']:
                i['attr_filter'] = i['attr_filter'].split(',')

            if i['type_id'] not in result:
                result[i['type_id']] = i
            else:
                if i['attr_filter']:
                    if not result[i['type_id']]['attr_filter']:
                        result[i['type_id']]['attr_filter'] = []

                    result[i['type_id']]['attr_filter'] += i['attr_filter']
                    result[i['type_id']]['attr_filter'] = list(set(i['attr_filter']))
                if i['ci_filter']:
                    if not result[i['type_id']]['ci_filter']:
                        result[i['type_id']]['ci_filter'] = ""
                    result[i['type_id']]['ci_filter'] += (i['ci_filter'] or "")

        return result

    @classmethod
    def get_attr_filter(cls, type_id):
        if is_app_admin('cmdb') or g.user.username in ('worker', 'cmdb_agent'):
            return []

        res2 = ACLManager('cmdb').get_resources(ResourceTypeEnum.CI_FILTER)
        if res2:
            type2filter_perms = cls().get_by_ids(list(map(int, [i['name'] for i in res2])), type_id=type_id)
            return type2filter_perms.get(type_id, {}).get('attr_filter') or []

    def _can_add(self, **kwargs):
        ci_filter = kwargs.get('ci_filter')
        attr_filter = kwargs.get('attr_filter') or ""

        if 'attr_filter' in kwargs:
            kwargs['attr_filter'] = kwargs['attr_filter'] or None

        if attr_filter:
            kwargs['attr_filter'] = ','.join(attr_filter or [])

        if ci_filter and not kwargs.get('name'):
            return abort(400, ErrFormat.ci_filter_name_cannot_be_empty)

        if ci_filter and ci_filter.startswith('q='):
            kwargs['ci_filter'] = kwargs['ci_filter'][2:]

        return kwargs

    def add(self, **kwargs):
        kwargs = self._can_add(**kwargs) or kwargs

        obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                              rid=kwargs.get('rid'),
                              first=True, to_dict=False)
        if obj is not None:
            obj = obj.update(filter_none=False, **kwargs)
            if not obj.attr_filter and not obj.ci_filter:
                if current_app.config.get('USE_ACL'):
                    ACLManager().del_resource(str(obj.id), ResourceTypeEnum.CI_FILTER)

                obj.soft_delete()

        else:
            if not kwargs.get('ci_filter') and not kwargs.get('attr_filter'):
                return

            obj = self.cls.create(**kwargs)

        if current_app.config.get('USE_ACL'):
            try:
                ACLManager().add_resource(obj.id, ResourceTypeEnum.CI_FILTER)
            except:
                pass
            ACLManager().grant_resource_to_role_by_rid(obj.id,
                                                       kwargs.get('rid'),
                                                       ResourceTypeEnum.CI_FILTER)

        return obj

    def _can_update(self, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        pass

    def delete(self, **kwargs):
        obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                              rid=kwargs.get('rid'),
                              first=True, to_dict=False)

        if obj is not None:
            if current_app.config.get('USE_ACL'):
                ACLManager().del_resource(str(obj.id), ResourceTypeEnum.CI_FILTER)

            obj.soft_delete()


def has_perm_for_ci(arg_name, resource_type, perm, callback=None, app=None):
    def decorator_has_perm(func):
        @functools.wraps(func)
        def wrapper_has_perm(*args, **kwargs):
            if not arg_name:
                return
            resource = request.view_args.get(arg_name) or request.values.get(arg_name)
            if callback is not None and resource:
                resource = callback(resource)

            if current_app.config.get("USE_ACL") and resource:
                if g.user.username == "worker" or g.user.username == "cmdb_agent":
                    request.values['__is_admin'] = True
                    return func(*args, **kwargs)

                if is_app_admin(app):
                    request.values['__is_admin'] = True
                    return func(*args, **kwargs)

                validate_permission(resource.name, resource_type, perm, app)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm
