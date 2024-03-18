# -*- coding:utf-8 -*-
import copy
import functools

import redis_lock
from flask import abort
from flask import current_app
from flask import request
from flask_login import current_user

from api.extensions import db
from api.extensions import rd
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

                if i['id_filter']:
                    if not result[i['rid']]['id_filter']:
                        result[i['rid']]['id_filter'] = {}
                    result[i['rid']]['id_filter'].update(i['id_filter'] or {})

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

                if i['id_filter']:
                    if not result[i['type_id']]['id_filter']:
                        result[i['type_id']]['id_filter'] = {}
                    result[i['type_id']]['id_filter'].update(i['id_filter'] or {})

        return result

    @classmethod
    def get_attr_filter(cls, type_id):
        if is_app_admin('cmdb') or current_user.username in ('worker', 'cmdb_agent'):
            return []

        res2 = ACLManager('cmdb').get_resources(ResourceTypeEnum.CI_FILTER)
        if res2:
            type2filter_perms = cls().get_by_ids(list(map(int, [i['name'] for i in res2])), type_id=type_id)
            return type2filter_perms.get(type_id, {}).get('attr_filter') or []

    def _revoke_children(self, rid, id_filter, rebuild=True):
        items = self.cls.get_by(rid=rid, ci_filter=None, attr_filter=None, to_dict=False)
        for item in items:
            changed, item_id_filter = False, copy.deepcopy(item.id_filter)
            for prefix in id_filter:
                for k, v in copy.deepcopy((item.id_filter or {})).items():
                    if k.startswith(prefix) and k != prefix:
                        item_id_filter.pop(k)
                        changed = True

            if not item_id_filter and current_app.config.get('USE_ACL'):
                item.soft_delete(commit=False)
                ACLManager().del_resource(str(item.id), ResourceTypeEnum.CI_FILTER, rebuild=rebuild)
            elif changed:
                item.update(id_filter=item_id_filter, commit=False)

        db.session.commit()

    def _revoke_parent(self, rid, parent_path, rebuild=True):
        parent_path = [i for i in parent_path.split(',') if i] or []
        revoke_nodes = [','.join(parent_path[:i]) for i in range(len(parent_path), 0, -1)]
        for node_path in revoke_nodes:
            delete_item, can_deleted = None, True
            items = self.cls.get_by(rid=rid, ci_filter=None, attr_filter=None, to_dict=False)
            for item in items:
                if node_path in item.id_filter:
                    delete_item = item
                if any(filter(lambda x: x.startswith(node_path) and x != node_path, item.id_filter.keys())):
                    can_deleted = False
                    break

            if can_deleted and delete_item:
                id_filter = copy.deepcopy(delete_item.id_filter)
                id_filter.pop(node_path)
                delete_item = delete_item.update(id_filter=id_filter, filter_none=False)

                if current_app.config.get('USE_ACL') and not id_filter:
                    ACLManager().del_resource(str(delete_item.id), ResourceTypeEnum.CI_FILTER, rebuild=False)
                    delete_item.soft_delete()
                    items.remove(delete_item)

        if rebuild:
            from api.tasks.acl import role_rebuild
            from api.lib.perm.acl.const import ACL_QUEUE
            from api.lib.perm.acl.cache import AppCache

            role_rebuild.apply_async(args=(rid, AppCache.get('cmdb').id), queue=ACL_QUEUE)

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
        with redis_lock.Lock(rd.r, 'CMDB_FILTER_{}_{}'.format(kwargs['type_id'], kwargs['rid'])):
            request_id_filter = {}
            if kwargs.get('id_filter'):
                obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                                      rid=kwargs.get('rid'),
                                      ci_filter=None,
                                      attr_filter=None,
                                      first=True, to_dict=False)

                for _id, v in (kwargs.get('id_filter') or {}).items():
                    key = ",".join(([v['parent_path']] if v.get('parent_path') else []) + [str(_id)])
                    request_id_filter[key] = v['name']

            else:
                obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                                      rid=kwargs.get('rid'),
                                      id_filter=None,
                                      first=True, to_dict=False)

            is_recursive = kwargs.pop('is_recursive', 0)
            if obj is not None:
                if obj.id_filter and isinstance(kwargs.get('id_filter'), dict):
                    obj_id_filter = copy.deepcopy(obj.id_filter)

                    for k, v in request_id_filter.items():
                        obj_id_filter[k] = v

                    kwargs['id_filter'] = obj_id_filter

                obj = obj.update(filter_none=False, **kwargs)

                if not obj.attr_filter and not obj.ci_filter and not obj.id_filter:
                    if current_app.config.get('USE_ACL'):
                        ACLManager().del_resource(str(obj.id), ResourceTypeEnum.CI_FILTER, rebuild=False)

                    obj.soft_delete()

                if not is_recursive and request_id_filter:
                    self._revoke_children(obj.rid, request_id_filter, rebuild=False)

                return

            else:
                if not kwargs.get('ci_filter') and not kwargs.get('attr_filter') and not kwargs.get('id_filter'):
                    return

                if request_id_filter:
                    kwargs['id_filter'] = request_id_filter

                obj = self.cls.create(**kwargs)

                if current_app.config.get('USE_ACL'):  # new resource
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
        with redis_lock.Lock(rd.r, 'CMDB_FILTER_{}_{}'.format(kwargs['type_id'], kwargs['rid'])):
            obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                                  rid=kwargs.get('rid'),
                                  id_filter=None,
                                  first=True, to_dict=False)

            if obj is not None:
                resource = None
                if current_app.config.get('USE_ACL'):
                    resource = ACLManager().del_resource(str(obj.id), ResourceTypeEnum.CI_FILTER)

                obj.soft_delete()

                return resource

    def delete2(self, **kwargs):

        with redis_lock.Lock(rd.r, 'CMDB_FILTER_{}_{}'.format(kwargs['type_id'], kwargs['rid'])):
            obj = self.cls.get_by(type_id=kwargs.get('type_id'),
                                  rid=kwargs.get('rid'),
                                  ci_filter=None,
                                  attr_filter=None,
                                  first=True, to_dict=False)

            request_id_filter = {}
            for _id, v in (kwargs.get('id_filter') or {}).items():
                key = ",".join([v['parent_path']] if v.get('parent_path') else [] + [str(_id)])
                request_id_filter[key] = v['name']

            resource = None
            if obj is not None:

                id_filter = {}
                for k, v in copy.deepcopy(obj.id_filter or {}).items():  # important
                    if k not in request_id_filter:
                        id_filter[k] = v

                if not id_filter and current_app.config.get('USE_ACL'):
                    resource = ACLManager().del_resource(str(obj.id), ResourceTypeEnum.CI_FILTER, rebuild=False)
                    obj.soft_delete()
                    db.session.commit()

                else:
                    obj.update(id_filter=id_filter)

                self._revoke_children(kwargs.get('rid'), request_id_filter, rebuild=False)
                self._revoke_parent(kwargs.get('rid'), kwargs.get('parent_path'))

            return resource

    def delete_id_filter_by_ci_id(self, ci_id):
        items = self.cls.get_by(ci_filter=None, attr_filter=None, to_dict=False)

        rebuild_roles = set()
        for item in items:
            id_filter = copy.deepcopy(item.id_filter)
            changed = False
            for node_path in item.id_filter:
                if str(ci_id) in node_path:
                    id_filter.pop(node_path)
                    changed = True

            if changed:
                rebuild_roles.add(item.rid)
                if not id_filter:
                    item.soft_delete(commit=False)
                else:
                    item.update(id_filter=id_filter, commit=False)

        db.session.commit()

        if rebuild_roles:
            from api.tasks.acl import role_rebuild
            from api.lib.perm.acl.const import ACL_QUEUE
            from api.lib.perm.acl.cache import AppCache
            for rid in rebuild_roles:
                role_rebuild.apply_async(args=(rid, AppCache.get('cmdb').id), queue=ACL_QUEUE)


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
                if current_user.username == "worker" or current_user.username == "cmdb_agent":
                    request.values['__is_admin'] = True
                    return func(*args, **kwargs)

                if is_app_admin(app):
                    request.values['__is_admin'] = True
                    return func(*args, **kwargs)

                validate_permission(resource.name, resource_type, perm, app)

            return func(*args, **kwargs)

        return wrapper_has_perm

    return decorator_has_perm
