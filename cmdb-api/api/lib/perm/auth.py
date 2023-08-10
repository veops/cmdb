# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from functools import wraps

import jwt
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user

from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat
from api.models.acl import Role
from api.models.acl import User


def reset_session(user, role=None):
    from api.lib.perm.acl.acl import ACLManager
    if role is not None:
        user_info = ACLManager.get_user_info(role)
    else:
        user_info = ACLManager.get_user_info(user.username)

    session["acl"] = dict(uid=user_info.get("uid"),
                          avatar=user.avatar if user else user_info.get("avatar"),
                          userId=user_info.get("uid"),
                          userName=user_info.get("username"),
                          nickName=user_info.get("nickname"),
                          parentRoles=user_info.get("parents"),
                          childRoles=user_info.get("children"),
                          roleName=user_info.get("role"))
    session["uid"] = user_info.get("uuid")


def _auth_with_key():
    key = request.values.get('_key')
    secret = request.values.get('_secret')
    if not key:
        return False

    path = request.path
    keys = sorted(request.values.keys())
    req_args = [str(request.values[k]) for k in keys if k not in ("_key", "_secret") and
                not isinstance(request.values[k], (dict, list))]
    user, authenticated = User.query.authenticate_with_key(key, secret, req_args, path)
    if user and authenticated:
        login_user(user)
        reset_session(user)
        return True

    role, authenticated = Role.query.authenticate_with_key(key, secret, req_args, path)
    if role and authenticated:
        reset_session(None, role=role.name)
        return True

    return False


def _auth_with_session():
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
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.filter_by(email=data['sub']).first()
        if not user:
            return False

        login_user(user)
        reset_session(user)
        return True
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, Exception) as e:
        current_app.logger.error(str(e))
        return False


def _auth_with_ip_white_list():
    ip = request.headers.get('X-Real-IP') or request.remote_addr
    key = request.values.get('_key')
    secret = request.values.get('_secret')
    current_app.logger.info(ip)
    if not key and not secret and ip.strip() in current_app.config.get("WHITE_LIST", []):  # TODO
        user = UserCache.get("worker")
        login_user(user)
        return True
    return False


def _auth_with_app_token():
    if _auth_with_session() or _auth_with_token():
        if not is_app_admin(request.values.get('app_id')) and request.method != "GET":
            return False
        elif is_app_admin(request.values.get('app_id')):
            return True

    if _auth_with_key() and is_app_admin('acl'):
        return True

    auth_headers = request.headers.get('App-Access-Token', '').strip()
    if not auth_headers:
        return False

    try:
        token = auth_headers
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        current_app.logger.warning(data)
        app = AppCache.get(data['sub'])
        if not app:
            return False

        request.values['app_id'] = app.id

        return True
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, Exception) as e:
        current_app.logger.error(str(e))
        return False


def _auth_with_acl_token():
    token = request.headers.get('Authorization', "")
    if not token.startswith('Bearer '):
        abort(401, ErrFormat.unauthorized)

    _token = token.split(' ')[-1]

    result = ACLManager().authenticate_with_token(_token)
    if result.get('authenticated') and result.get('user'):
        user = User.query.filter_by(email=result.get("user", {}).get("email", "")).first()
        login_user(user)
        reset_session(user)
        return user
    elif result.get('authenticated') is False:
        abort(401, ErrFormat.unauthorized)


def auth_required(func):
    if request.get_json(silent=True) is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        if getattr(func, 'auth_only_with_app_token', False) and _auth_with_app_token():
            return func(*args, **kwargs)
        elif getattr(func, 'auth_only_with_app_token', False):
            if _auth_with_key() and is_app_admin('acl'):
                return func(*args, **kwargs)

            if request.headers.get('App-Access-Token', '').strip():
                return abort(403, ErrFormat.auth_only_with_app_token_failed)
            else:
                return abort(403, ErrFormat.session_invalid)

        if getattr(func, 'auth_with_app_token', False) and _auth_with_app_token():
            return func(*args, **kwargs)

        elif _auth_with_session() or _auth_with_key() or _auth_with_token() or _auth_with_ip_white_list():
            return func(*args, **kwargs)

        if _auth_with_acl_token():
            return func(*args, **kwargs)

        return abort(401, ErrFormat.unauthorized)

    return wrapper


def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def auth_with_app_token(func):
    setattr(func, 'auth_with_app_token', True)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def auth_only_for_acl(func):
    setattr(func, 'auth_only_with_app_token', True)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def auth_with_acl_token(func):
    setattr(func, 'auth_with_acl_token', True)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper()
