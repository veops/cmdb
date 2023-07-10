# -*- coding:utf-8 -*-

import datetime

import jwt
import six
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user, logout_user

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import User
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.auth import auth_abandoned
from api.lib.perm.auth import auth_with_app_token
from api.models.acl import Role
from api.resource import APIView


class LoginView(APIView):
    url_prefix = "/login"

    @args_required("username")
    @args_required("password")
    @auth_abandoned
    @args_validate(User)
    def post(self):
        username = request.values.get("username") or request.values.get("email")
        password = request.values.get("password")
        _role = None
        if current_app.config.get('AUTH_WITH_LDAP'):
            user, authenticated = User.query.authenticate_with_ldap(username, password)
        else:
            user, authenticated = User.query.authenticate(username, password)
            if not user:
                _role, authenticated = Role.query.authenticate(username, password)

        if not user and not _role:
            return abort(401, ErrFormat.user_not_found.format(username))

        if not authenticated:
            return abort(401, ErrFormat.invalid_password)

        if user:
            login_user(user)
            user.update(has_logined=True, last_login=datetime.datetime.now())

            token = jwt.encode({
                'sub': user.email,
                'iat': datetime.datetime.now(),
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=24 * 60 * 7)},
                current_app.config['SECRET_KEY'])

            username = username.split("@")[0]
            user_info = ACLManager.get_user_info(username)

            session["acl"] = dict(uid=user_info.get("uid"),
                                  avatar=user.avatar if user else user_info.get("avatar"),
                                  userId=user_info.get("uid"),
                                  rid=user_info.get("rid"),
                                  userName=user_info.get("username"),
                                  nickName=user_info.get("nickname"),
                                  parentRoles=user_info.get("parents"),
                                  childRoles=user_info.get("children"),
                                  roleName=user_info.get("role"))
            session["uid"] = user_info.get("uid")

            return self.jsonify(token=token.decode() if six.PY2 else token, username=username)
        else:
            return self.jsonify(username=username)


class AuthWithKeyView(APIView):
    url_prefix = "/auth_with_key"

    @args_required("key")
    @args_required("secret")
    @args_required("path")
    @auth_abandoned
    def post(self):
        key = request.values.get('key')
        secret = request.values.get('secret')
        path = six.moves.urllib.parse.urlparse(request.values.get('path')).path
        payload = request.values.get('payload') or {}

        payload.pop('_key', None)
        payload.pop('_secret', None)

        req_args = [str(payload[k]) for k in sorted(payload.keys())]
        user, authenticated = User.query.authenticate_with_key(key, secret, req_args, path)
        if user:
            role = RoleCache.get_by_name(None, user.username)
            role or abort(404, ErrFormat.role_not_found.format(user.username))
            user = user.to_dict()
        else:
            role, authenticated = Role.query.authenticate_with_key(key, secret, req_args, path)
            user = role and role.to_dict() or {}

        can_proxy = True if role and role.is_app_admin else False

        if can_proxy and request.values.get('proxy'):
            role = RoleCache.get_by_name(None, request.values.get('proxy'))
            role or abort(404, ErrFormat.role_not_found.format(request.values.get('proxy')))
            user = role and role.to_dict() or {}

        user['rid'] = role and role.id
        user.pop('password', None)
        user.pop('key', None)
        user.pop('secret', None)

        if not user.get('username'):
            user['username'] = user.get('name')

        return self.jsonify(user=user,
                            authenticated=authenticated,
                            rid=role and role.id,
                            can_proxy=can_proxy)


class AuthWithTokenView(APIView):
    url_prefix = ("/auth_with_token", "/req_token")

    @auth_with_app_token
    def get(self):
        username = request.values.get('username')

        token = jwt.encode({
            'sub': username,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=2 * 60)},
            current_app.config['SECRET_KEY'])

        return self.jsonify(token=token)

    @args_required("token")
    @auth_with_app_token
    def post(self):
        token = request.values.get('token')

        user = None
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            authenticated = True
            user = UserCache.get(data.get('sub'))
            if not user:
                authenticated = False
        except jwt.ExpiredSignatureError:
            authenticated = False
        except (jwt.InvalidTokenError, Exception) as e:
            current_app.logger.error(str(e))
            authenticated = False

        if user is not None:
            role = RoleCache.get_by_name(None, user.username)
            role or abort(404, ErrFormat.role_not_found.format(user.username))
            user = user.to_dict()

            user['rid'] = role and role.id
            user.pop('password', None)
            user.pop('key', None)
            user.pop('secret', None)

        return self.jsonify(user=user,
                            authenticated=authenticated)


class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)
