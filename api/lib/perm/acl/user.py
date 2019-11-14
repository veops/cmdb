# -*- coding:utf-8 -*-


from flask import abort

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
    def add(**kwargs):
        existed = User.get_by(username=kwargs['username'], email=kwargs['email'])
        existed and abort(400, "User <{0}> is already existed".format(kwargs['username']))

        kwargs['nickname'] = kwargs['username'] if not kwargs.get('nickname') else kwargs['nickname']
        kwargs['block'] = 0
        return User.create(**kwargs)

    @staticmethod
    def update(rid, **kwargs):
        user = User.get_by_id(rid) or abort(404, "User <{0}> does not exist".format(rid))

        UserCache.clean(rid)

        return user.update(**kwargs)

    @classmethod
    def delete(cls, uid):
        user = User.get_by_id(uid) or abort(404, "User <{0}> does not exist".format(uid))

        UserCache.clean(user)

        user.soft_delete()
