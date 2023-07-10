# -*- coding:utf-8 -*-

import datetime

import six
import jwt
from flask import abort
from flask import current_app
from flask import request
from flask_login import login_user, logout_user

from api.lib.decorator import args_required
from api.lib.perm.acl.cache import User
from api.lib.perm.auth import auth_abandoned
from api.resource import APIView


class LoginView(APIView):
    url_prefix = "/login"

    @args_required("username")
    @args_required("password")
    @auth_abandoned
    def post(self):
        username = request.values.get("username") or request.values.get("email")
        password = request.values.get("password")
        user, authenticated = User.query.authenticate(username, password)
        if not authenticated:
            return abort(401, "invalid username or password")

        login_user(user)

        token = jwt.encode({
            'sub': user.email,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=24 * 60 * 7)},
            current_app.config['SECRET_KEY'])

        return self.jsonify(token=token.decode() if six.PY2 else token, username=username)


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

        return self.jsonify(user=user.to_dict() if user else {},
                            authenticated=authenticated)


class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)
