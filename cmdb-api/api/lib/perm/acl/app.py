# -*- coding:utf-8 -*-

import datetime
import hashlib

import jwt
from flask import abort
from flask import current_app

from api.extensions import db
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.audit import AuditOperateType
from api.lib.perm.acl.audit import AuditScope
from api.lib.perm.acl.resp_format import ErrFormat
from api.models.acl import App


class AppCRUD(object):
    cls = App

    @staticmethod
    def get_all():
        return App.get_by(to_dict=False)

    @staticmethod
    def get(app_id):
        return App.get_by_id(app_id)

    @staticmethod
    def search(q, page=1, page_size=None):
        query = db.session.query(App).filter(App.deleted.is_(False))
        if q:
            query = query.filter(App.name.ilike('%{0}%'.format(q)))

        numfound = query.count()
        res = query.offset((page - 1) * page_size).limit(page_size)

        return numfound, res

    @classmethod
    def add(cls, name, description):
        App.get_by(name=name) and abort(400, ErrFormat.app_is_ready_existed.format(name))

        from api.lib.perm.acl.user import UserCRUD
        app_id, secret_key = UserCRUD.gen_key_secret()

        app = App.create(name=name, description=description, app_id=app_id, secret_key=secret_key)
        AuditCRUD.add_resource_log(app.id, AuditOperateType.create, AuditScope.app, app.id, {}, app.to_dict(), {})
        return app

    @classmethod
    def update(cls, _id, **kwargs):
        kwargs.pop('id', None)

        existed = App.get_by_id(_id) or abort(404, ErrFormat.app_not_found.format("id={}".format(_id)))

        origin = existed.to_dict()
        existed = existed.update(**kwargs)

        AuditCRUD.add_resource_log(existed.id, AuditOperateType.update,
                                   AuditScope.app, existed.id, origin, existed.to_dict(), {})

        return existed

    @classmethod
    def delete(cls, _id):
        app = App.get_by_id(_id) or abort(404, ErrFormat.app_not_found.format("id={}".format(_id)))
        origin = app.to_dict()

        app.soft_delete()

        AuditCRUD.add_resource_log(app.id, AuditOperateType.delete,
                                   AuditScope.app, app.id, origin, {}, {})

    @staticmethod
    def _get_by_key(key):
        return App.get_by(app_id=key, first=True, to_dict=False)

    @classmethod
    def gen_token(cls, key, secret):
        app = cls._get_by_key(key) or abort(404, ErrFormat.app_not_found.format("key={}".format(key)))
        secret != hashlib.md5(app.secret_key.encode('utf-8')).hexdigest() and abort(403, ErrFormat.app_secret_invalid)

        token = jwt.encode({
            'sub': app.name,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=2 * 60)},
            current_app.config['SECRET_KEY'])

        try:
            return token.decode()
        except AttributeError:
            return token
