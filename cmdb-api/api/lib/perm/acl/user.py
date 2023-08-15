# -*- coding:utf-8 -*-


import random
import string
import uuid

from flask import abort
from flask_login import current_user

from api.extensions import db
from api.lib.perm.acl.audit import AuditCRUD, AuditOperateType, AuditScope
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.role import RoleCRUD
from api.models.acl import Role
from api.models.acl import User


class UserCRUD(object):
    cls = User

    @staticmethod
    def search(q, page=1, page_size=None):
        query = db.session.query(User).filter(User.deleted.is_(False))
        if q:
            query = query.filter(User.username.ilike('%{0}%'.format(q)))

        numfound = query.count()

        return numfound, query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def gen_key_secret():
        key = uuid.uuid4().hex
        secret = ''.join(random.sample(string.ascii_letters + string.digits + '~!@#$%^&*?', 32))

        return key, secret

    @classmethod
    def add(cls, **kwargs):
        existed = User.get_by(username=kwargs['username'], email=kwargs['email'])
        existed and abort(400, ErrFormat.user_exists.format(kwargs['username']))

        kwargs['nickname'] = kwargs.get('nickname') or kwargs['username']
        kwargs['block'] = 0
        kwargs['key'], kwargs['secret'] = cls.gen_key_secret()

        user_employee = db.session.query(User).filter(User.deleted.is_(False)).order_by(
            User.employee_id.desc()).first()

        biggest_employee_id = int(float(user_employee.employee_id)) \
            if user_employee is not None else 0

        kwargs['employee_id'] = '{0:04d}'.format(biggest_employee_id + 1)
        user = User.create(**kwargs)

        RoleCRUD.add_role(user.username, uid=user.uid)
        AuditCRUD.add_role_log(None, AuditOperateType.create,
                               AuditScope.user, user.uid, {}, user.to_dict(), {}, {}
                               )

        return user

    @staticmethod
    def update(uid, **kwargs):
        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(
            404, ErrFormat.user_not_found.format("uid={}".format(uid)))

        if kwargs.get("username"):
            other = User.get_by(username=kwargs['username'], first=True, to_dict=False)
            if other is not None and other.uid != user.uid:
                return abort(400, ErrFormat.user_exists.format(kwargs['username']))

        UserCache.clean(user)
        origin = user.to_dict()
        if kwargs.get("username") and kwargs['username'] != user.username:
            role = Role.get_by(name=user.username, first=True, to_dict=False)
            if role is not None:
                RoleCRUD.update_role(role.id, **dict(name=kwargs['username']))

        user = user.update(**kwargs)

        AuditCRUD.add_role_log(None, AuditOperateType.update,
                               AuditScope.user, user.uid, origin, user.to_dict(), {}, {}
                               )

        return user

    @classmethod
    def reset_key_secret(cls):
        key, secret = cls.gen_key_secret()
        current_user.update(key=key, secret=secret)

        UserCache.clean(current_user)

        return key, secret

    @classmethod
    def delete(cls, uid):
        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(
            404, ErrFormat.user_not_found.format("uid={}".format(uid)))

        origin = user.to_dict()

        user.soft_delete()

        UserCache.clean(user)

        role = RoleCRUD.get_by_name(user.username, app_id=None)
        if role:
            RoleCRUD.delete_role(role[0]['id'], force=True)

        AuditCRUD.add_role_log(None, AuditOperateType.delete,
                               AuditScope.user, user.uid, origin, {}, {}, {})

    @staticmethod
    def get_employees():
        return User.get_by(__func_isnot__key_employee_id=None, to_dict=True)
