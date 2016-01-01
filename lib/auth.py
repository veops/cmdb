# -*- coding:utf-8 -*- 

import urllib
from functools import wraps

from flask import current_app
from flask import g
from flask import request
from flask import abort
from flask.ext.principal import identity_changed
from flask.ext.principal import Identity
from flask.ext.principal import AnonymousIdentity

from models.account import User
from models.account import UserCache


def auth_with_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(getattr(g, 'user', None), User):
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(g.user.uid))
            return func(*args, **kwargs)
        ip = request.remote_addr
        if request.data:
            request_args = dict()
            _args = request.data.split("&")
            for arg in _args:
                if arg:
                    request_args[arg.split("=")[0]] = \
                        urllib.unquote(arg.split("=")[1])
        else:
            request_args = request.values

        key = request_args.get('_key')
        secret = request_args.get('_secret')
        if not key and not secret and \
                ip.strip() in current_app.config.get("WHITE_LIST"):
            ip = ip.strip()
            user = UserCache.get(ip)
            if user:
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.uid))
                return func(*args, **kwargs)
            else:
                identity_changed.send(current_app._get_current_object(),
                                      identity=AnonymousIdentity())
                return abort(400, "invalid _key and _secret")

        path = request.path

        keys = sorted(request_args.keys())
        req_args = [request_args[k] for k in keys
                    if str(k) not in ("_key", "_secret")]
        current_app.logger.debug('args is %s' % req_args)
        user, authenticated = User.query.authenticate_with_key(
            key, secret, req_args, path)
        if user and authenticated:
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.get("uid")))
            return func(*args, **kwargs)
        else:
            identity_changed.send(current_app._get_current_object(),
                                  identity=AnonymousIdentity())
            return abort(400, "invalid _key and _secret")

    return wrapper
