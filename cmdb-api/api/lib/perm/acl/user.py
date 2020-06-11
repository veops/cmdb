# -*- coding:utf-8 -*-


import random
import string
import uuid

from flask import abort
from flask import g

from api.extensions import db
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.role import RoleCRUD
from api.models.acl import Role
from api.models.acl import User


class UserCRUD(object):
    @staticmethod
    def search(q, page=1, page_size=None):
        query = db.session.query(User).filter(User.deleted.is_(False))
        if q:
            query = query.filter(User.username.ilike('%{0}%'.format(q)))

        numfound = query.count()

        return numfound, query.offset((page - 1) * page_size).limit(page_size)

    @staticmethod
    def _gen_key_secret():
        key = uuid.uuid4().hex
        secret = ''.join(random.sample(string.ascii_letters + string.digits + '~!@#$%^&*?', 32))

        return key, secret

    @classmethod
    def add(cls, **kwargs):
        existed = User.get_by(username=kwargs['username'], email=kwargs['email'])
        existed and abort(400, "User <{0}> is already existed".format(kwargs['username']))

        is_admin = kwargs.pop('is_admin', False)
        kwargs['nickname'] = kwargs.get('nickname') or kwargs['username']
        kwargs['block'] = 0
        kwargs['key'], kwargs['secret'] = cls._gen_key_secret()

        user = User.create(**kwargs)

        role = RoleCRUD.add_role(user.username, uid=user.uid)

        if is_admin:
            from api.lib.perm.acl.cache import AppCache
            from api.lib.perm.acl.role import RoleRelationCRUD
            admin_r = Role.get_by(name='admin', first=True, to_dict=False) or \
                      RoleCRUD.add_role('admin', AppCache.get('cmdb').id, True)

            RoleRelationCRUD.add(admin_r.id, role.id)

        return user

    @staticmethod
    def update(uid, **kwargs):
        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(404, "User <{0}> does not exist".format(uid))

        if kwargs.get("username"):
            other = User.get_by(username=kwargs['username'], first=True, to_dict=False)
            if other is not None and other.uid != user.uid:
                return abort(400, "User <{0}> cannot be duplicated".format(kwargs['username']))

        UserCache.clean(user)

        if kwargs.get("username") and kwargs['username'] != user.username:
            role = Role.get_by(name=user.username, first=True, to_dict=False)
            if role is not None:
                RoleCRUD.update_role(role.id, **dict(name=kwargs['name']))

        return user.update(**kwargs)

    @classmethod
    def reset_key_secret(cls):
        key, secret = cls._gen_key_secret()
        g.user.update(key=key, secret=secret)

        return key, secret

    @classmethod
    def delete(cls, uid):
        if hasattr(g, 'user') and uid == g.user.uid:
            return abort(400, "You cannot delete yourself")

        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(404, "User <{0}> does not exist".format(uid))

        UserCache.clean(user)

        for i in Role.get_by(uid=uid, to_dict=False):
            i.delete()

        user.delete()
