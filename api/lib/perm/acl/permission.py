# -*- coding:utf-8 -*-


from api.lib.perm.acl.cache import PermissionCache
from api.lib.perm.acl.cache import RoleCache
from api.models.acl import RolePermission


class PermissionCRUD(object):
    @staticmethod
    def get_all(resource_id=None, group_id=None):
        result = dict()
        if resource_id is not None:
            perms = RolePermission.get_by(resource_id=resource_id, to_dict=False)
        else:
            perms = RolePermission.get_by(group_id=group_id, to_dict=False)

        for perm in perms:
            result.setdefault((perm.rid, RoleCache.get(perm.rid).name), []).append(
                PermissionCache.get(perm.perm_id).to_dict())

        return result

    @staticmethod
    def grant(rid, perms, resource_id=None, group_id=None):
        for perm in perms:
            perm = PermissionCache.get(perm)
            existed = RolePermission.get_by(rid=rid, perm_id=perm.id, group_id=group_id, resource_id=resource_id)
            existed or RolePermission.create(rid=rid, perm_id=perm.id, group_id=group_id, resource_id=resource_id)

    @staticmethod
    def revoke(rid, perms, resource_id=None, group_id=None):
        for perm in perms:
            perm = PermissionCache.get(perm)
            existed = RolePermission.get_by(rid=rid,
                                            perm_id=perm.id,
                                            group_id=group_id,
                                            resource_id=resource_id,
                                            first=True,
                                            to_dict=False)
            existed and existed.soft_delete()
