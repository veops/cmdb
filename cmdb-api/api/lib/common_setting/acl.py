# -*- coding:utf-8 -*-
from flask import abort
from flask import current_app

from api.lib.common_setting.resp_format import ErrFormat
from api.lib.perm.acl.cache import RoleCache, AppCache
from api.lib.perm.acl.role import RoleCRUD, RoleRelationCRUD
from api.lib.perm.acl.user import UserCRUD


class ACLManager(object):
    def __init__(self, app_name='acl', uid=None):
        self.log = current_app.logger
        self.app_name = app_name
        self.uid = uid

    @staticmethod
    def get_all_users():
        try:
            numfound, users = UserCRUD.search(None, 1, 999999)
            users = [i.to_dict() for i in users]
            for u in users:
                u.pop('password', None)
                u.pop('key', None)
                u.pop('secret', None)
            return users
        except Exception as e:
            current_app.logger.error(str(e))
            raise Exception(ErrFormat.acl_get_all_users_failed.format(str(e)))

    @staticmethod
    def create_user(payload):
        user = UserCRUD.add(**payload)
        return user.to_dict()

    @staticmethod
    def edit_user(uid, payload):
        user = UserCRUD.update(uid, **payload)
        return user.to_dict()

    def get_all_roles(self):
        numfound, roles = RoleCRUD.search(
            None, self.app_name, 1, 999999, True, True, False)

        return [i.to_dict() for i in roles]

    def remove_user_from_role(self, user_rid, payload):
        app_id = self.app_name
        app = AppCache.get(app_id)
        if app and app.name == "acl":
            app_id = None  # global

        RoleRelationCRUD.delete2(
            payload.get('parent_id'), user_rid, app_id)
        return dict(
            message="success"
        )

    def add_user_to_role(self, role_id, payload):
        app_id = self.app_name
        app = AppCache.get(self.app_name)
        if app and app.name == "acl":
            app_id = None
        role = RoleCache.get(role_id)
        res = RoleRelationCRUD.add(
            role, role_id, payload['child_ids'], app_id)
        return res

    @staticmethod
    def create_role(payload):
        payload['is_app_admin'] = payload.get('is_app_admin', False)
        role = RoleCRUD.add_role(**payload)
        return role.to_dict()

    @staticmethod
    def edit_role(_id, payload):
        role = RoleCRUD.update_role(_id, **payload)
        return role.to_dict()

    @staticmethod
    def delete_role(_id, payload):
        RoleCRUD.delete_role(_id)
        return dict(rid=_id)

    def get_user_info(self, username):
        from api.lib.perm.acl.acl import ACLManager as ACL
        user_info = ACL().get_user_info(username, self.app_name)
        result = dict(name=user_info.get('nickname') or username,
                      username=user_info.get('username') or username,
                      email=user_info.get('email'),
                      uid=user_info.get('uid'),
                      rid=user_info.get('rid'),
                      role=dict(permissions=user_info.get('parents')),
                      avatar=user_info.get('avatar'))

        return result
