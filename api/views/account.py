# -*- coding:utf-8 -*-

import datetime

import jwt
from flask import request
from flask import current_app
from flask import abort
from flask_login import login_user, logout_user

from api.resource import APIView
from api.lib.decorator import args_required
from api.lib.perm.auth import auth_abandoned
from api.models.account import User


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

        return self.jsonify(token=token.decode())


class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)
