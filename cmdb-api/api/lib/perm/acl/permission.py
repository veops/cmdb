# -*- coding:utf-8 -*-
import datetime

from flask import abort

from api.extensions import db
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.audit import AuditOperateSource
from api.lib.perm.acl.audit import AuditOperateType
from api.lib.perm.acl.cache import PermissionCache
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.role import RoleRelationCRUD
from api.models.acl import Resource
from api.models.acl import ResourceGroup
from api.models.acl import ResourceType
from api.models.acl import RolePermission
from api.tasks.acl import role_rebuild


class PermissionCRUD(object):
    @staticmethod
    def get_all(resource_id=None, group_id=None, need_users=True):
        result = dict()

        if resource_id is not None:
            r = Resource.get_by_id(resource_id)
            if not r:
                return result
            rt_id = r.resource_type_id
            perms = RolePermission.get_by(resource_id=resource_id, to_dict=False)
        else:
            rg = ResourceGroup.get_by_id(group_id)
            if not rg:
                return result
            rt_id = rg.resource_type_id
            perms = RolePermission.get_by(group_id=group_id, to_dict=False)

        rid2obj = dict()
        uid2obj = dict()
        for perm in perms:
            perm_dict = PermissionCache.get(perm.perm_id, rt_id)
            perm_dict = perm_dict and perm_dict.to_dict()
            if not perm_dict:
                continue
            perm_dict.update(dict(rid=perm.rid))

            if perm.rid not in rid2obj:
                rid2obj[perm.rid] = RoleCache.get(perm.rid)

            role = rid2obj[perm.rid]
            if role and role.uid:
                if role.uid not in uid2obj:
                    uid2obj[role.uid] = UserCache.get(role.uid)

                name = uid2obj[role.uid].nickname
            elif role:
                name = role.name
            else:
                continue

            result.setdefault(name,
                              dict(perms=[],
                                   users=RoleRelationCRUD.get_users_by_rid(perm.rid, perm.app_id, rid2obj, uid2obj)
                                   if need_users else [])
                              )['perms'].append(perm_dict)

        return result

    @classmethod
    def get_all2(cls, resource_name, resource_type_name, app_id):
        rt = ResourceType.get_by(name=resource_type_name, first=True, to_dict=False)
        rt or abort(404, ErrFormat.resource_type_not_found.format(resource_type_name))

        r = Resource.get_by(name=resource_name, resource_type_id=rt.id, app_id=app_id, first=True, to_dict=False)

        return r and cls.get_all(r.id)

    @staticmethod
    def grant(rid, perms, resource_id=None, group_id=None, rebuild=True, source=AuditOperateSource.acl):
        app_id = None
        rt_id = None

        from api.lib.perm.acl.resource import ResourceTypeCRUD

        if resource_id is not None:
            from api.models.acl import Resource

            resource = Resource.get_by_id(resource_id) or abort(404, ErrFormat.resource_not_found.format(
                "id={}".format(resource_id)))

            app_id = resource.app_id
            rt_id = resource.resource_type_id
            if not perms:
                perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(resource.resource_type_id)]

        elif group_id is not None:
            from api.models.acl import ResourceGroup

            group = ResourceGroup.get_by_id(group_id) or abort(
                404, ErrFormat.resource_group_not_found.format("id={}".format(group_id)))
            app_id = group.app_id
            rt_id = group.resource_type_id
            if not perms:
                perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(group.resource_type_id)]

        _role_permissions = []

        for _perm in set(perms):
            perm = PermissionCache.get(_perm, rt_id)
            if not perm:
                continue

            existed = RolePermission.get_by(rid=rid,
                                            app_id=app_id,
                                            perm_id=perm.id,
                                            group_id=group_id,
                                            resource_id=resource_id)

            if not existed:
                __role_permission = RolePermission.create(rid=rid,
                                                          app_id=app_id,
                                                          perm_id=perm.id,
                                                          group_id=group_id,
                                                          resource_id=resource_id)
                _role_permissions.append(__role_permission)

        if rebuild:
            role_rebuild.apply_async(args=(rid, app_id), queue=ACL_QUEUE)

        AuditCRUD.add_permission_log(app_id, AuditOperateType.grant, rid, rt_id, _role_permissions,
                                     source=source)

    @staticmethod
    def batch_grant_by_resource_names(rid, perms, resource_type_id, resource_names,
                                      resource_ids=None, perm_map=None, app_id=None):

        from api.lib.perm.acl.resource import ResourceTypeCRUD

        if resource_names:
            resource_ids = []
            from api.models.acl import Resource

            for n in resource_names:
                resource = Resource.get_by(name=n, resource_type_id=resource_type_id, first=True, to_dict=False)
                if resource:
                    app_id = resource.app_id
                    if not perms:
                        perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(resource.resource_type_id)]

                    resource_ids.append(resource.id)
        resource_ids = resource_ids or []

        _role_permissions = []
        if isinstance(perm_map, dict):
            perm2resource = dict()
            for resource_id in resource_ids:
                for _perm in (perm_map.get(str(resource_id)) or []):
                    perm2resource.setdefault(_perm, []).append(resource_id)
            for _perm in perm2resource:
                perm = PermissionCache.get(_perm, resource_type_id)
                existeds = RolePermission.get_by(rid=rid,
                                                 app_id=app_id,
                                                 perm_id=perm.id,
                                                 __func_in___key_resource_id=perm2resource[_perm],
                                                 to_dict=False)

                for resource_id in (set(perm2resource[_perm]) - set([i.resource_id for i in existeds])):
                    _role_permission = RolePermission.create(flush=False,
                                                             commit=False,
                                                             rid=rid,
                                                             app_id=app_id,
                                                             perm_id=perm.id,
                                                             resource_id=resource_id,
                                                             )
                    _role_permissions.append(_role_permission)

            db.session.commit()

        else:
            for _perm in perms:
                perm = PermissionCache.get(_perm, resource_type_id)
                for resource_id in resource_ids:
                    existed = RolePermission.get_by(rid=rid,
                                                    app_id=app_id,
                                                    perm_id=perm.id,
                                                    resource_id=resource_id)

                    if not existed:
                        _role_permission = RolePermission.create(rid=rid,
                                                                 app_id=app_id,
                                                                 perm_id=perm.id,
                                                                 resource_id=resource_id)
                        _role_permissions.append(_role_permission)

        role_rebuild.apply_async(args=(rid, app_id), queue=ACL_QUEUE)

        AuditCRUD.add_permission_log(app_id, AuditOperateType.grant, rid, resource_type_id, _role_permissions)

    @staticmethod
    def revoke(rid, perms, resource_id=None, group_id=None, rebuild=True, source=AuditOperateSource.acl):
        app_id = None
        rt_id = None

        from api.lib.perm.acl.resource import ResourceTypeCRUD
        if resource_id is not None:
            from api.models.acl import Resource

            resource = Resource.get_by_id(resource_id) or abort(
                404, ErrFormat.resource_not_found.format("id={}".format(resource_id)))
            app_id = resource.app_id
            rt_id = resource.resource_type_id
            if not perms:
                perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(resource.resource_type_id)]

        elif group_id is not None:
            from api.models.acl import ResourceGroup

            group = ResourceGroup.get_by_id(group_id) or abort(
                404, ErrFormat.resource_group_not_found.format("id={}".format(group_id)))
            app_id = group.app_id

            rt_id = group.resource_type_id
            if not perms:
                perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(group.resource_type_id)]
        _role_permissions = []

        for perm in perms:
            perm = PermissionCache.get(perm, rt_id)
            if not perm:
                continue
            existed = RolePermission.get_by(rid=rid,
                                            perm_id=perm.id,
                                            group_id=group_id,
                                            resource_id=resource_id,
                                            first=True,
                                            to_dict=False)
            if existed:
                existed.soft_delete()
                _role_permissions.append(existed)

        if rebuild:
            role_rebuild.apply_async(args=(rid, app_id), queue=ACL_QUEUE)

        AuditCRUD.add_permission_log(app_id, AuditOperateType.revoke, rid, rt_id, _role_permissions,
                                     source=source)

    @staticmethod
    def batch_revoke_by_resource_names(rid, perms, resource_type_id, resource_names,
                                       resource_ids=None, perm_map=None, app_id=None):

        from api.lib.perm.acl.resource import ResourceTypeCRUD
        if resource_names:
            resource_ids = []
            from api.models.acl import Resource

            for n in resource_names:
                resource = Resource.get_by(name=n, resource_type_id=resource_type_id, first=True, to_dict=False)
                if resource:
                    app_id = resource.app_id
                    if not perms:
                        perms = [i.get('name') for i in ResourceTypeCRUD.get_perms(resource.resource_type_id)]

                    resource_ids.append(resource.id)
        resource_ids = resource_ids or []

        _role_permissions = []
        if isinstance(perm_map, dict):
            perm2resource = dict()
            for resource_id in resource_ids:
                for _perm in (perm_map.get(str(resource_id)) or []):
                    perm2resource.setdefault(_perm, []).append(resource_id)
            for _perm in perm2resource:
                perm = PermissionCache.get(_perm, resource_type_id)
                existeds = RolePermission.get_by(rid=rid,
                                                 app_id=app_id,
                                                 perm_id=perm.id,
                                                 __func_in___key_resource_id=perm2resource[_perm],
                                                 to_dict=False)
                for existed in existeds:
                    existed.deleted = True
                    existed.deleted_at = datetime.datetime.now()
                    db.session.add(existed)
                    _role_permissions.append(existed)

            db.session.commit()
        else:
            for _perm in perms:
                perm = PermissionCache.get(_perm, resource_type_id)
                for resource_id in resource_ids:
                    existed = RolePermission.get_by(rid=rid,
                                                    app_id=app_id,
                                                    perm_id=perm.id,
                                                    resource_id=resource_id,
                                                    first=True, to_dict=False)
                    if existed:
                        existed.soft_delete()
                        _role_permissions.append(existed)

        role_rebuild.apply_async(args=(rid, app_id), queue=ACL_QUEUE)

        AuditCRUD.add_permission_log(app_id, AuditOperateType.revoke, rid, resource_type_id, _role_permissions)
