# -*- coding:utf-8 -*-


import uuid
import string
import random

from flask import abort
from flask import g

from api.extensions import db
from api.lib.perm.acl.cache import UserCache
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

        kwargs['nickname'] = kwargs.get('nickname') or kwargs['username']
        kwargs['block'] = 0
        kwargs['key'], kwargs['secret'] = cls._gen_key_secret()

        return User.create(**kwargs)

    @staticmethod
    def update(uid, **kwargs):
        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(404, "User <{0}> does not exist".format(uid))

        UserCache.clean(uid)

        return user.update(**kwargs)

    @classmethod
    def reset_key_secret(cls):
        key, secret = cls._gen_key_secret()
        g.user.update(key=key, secret=secret)

        return key, secret

    @classmethod
    def delete(cls, uid):
        user = User.get_by(uid=uid, to_dict=False, first=True) or abort(404, "User <{0}> does not exist".format(uid))

        UserCache.clean(user)

        user.soft_delete()
