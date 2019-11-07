# -*- coding:utf-8 -*- 


from functools import wraps

import jwt
from flask import abort
from flask import current_app
from flask import g
from flask import request
from flask import session
from flask_login import login_user

from api.models.account import User
from api.models.account import UserCache


def _auth_with_key():
    key = request.values.get('_key')
    secret = request.values.get('_secret')
    path = request.path
    keys = sorted(request.values.keys())
    req_args = [request.values[k] for k in keys if str(k) not in ("_key", "_secret")]
    user, authenticated = User.query.authenticate_with_key(key, secret, req_args, path)
    if user and authenticated:
        login_user(user)
        return True
    return False


def _auth_with_session():
    if isinstance(getattr(g, 'user', None), User):
        login_user(g.user)
        return True
    if "acl" in session and "userName" in (session["acl"] or {}):
        login_user(UserCache.get(session["acl"]["userName"]))
        return True
    return False


def _auth_with_token():
    auth_headers = request.headers.get('Access-Token', '').strip()
    if not auth_headers:
        return False

    try:
        token = auth_headers
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = User.query.filter_by(email=data['sub']).first()
        if not user:
            return False

        login_user(user)
        return True
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, Exception):
        return False


def _auth_with_ip_white_list():
    ip = request.remote_addr
    key = request.values.get('_key')
    secret = request.values.get('_secret')

    if not key and not secret and ip.strip() in current_app.config.get("WHITE_LIST", []):  # TODO
        user = UserCache.get("worker")
        login_user(user)
        return True
    return False


def auth_required(func):
    if request.json is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    current_app.logger.debug(request.values)

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if _auth_with_session() or _auth_with_key() or _auth_with_token() or _auth_with_ip_white_list():
            return func(*args, **kwargs)

        abort(401)

    return wrapper


def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
