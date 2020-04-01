# -*- coding:utf-8 -*-

import datetime

import jwt
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user, logout_user

from api.lib.decorator import args_required
from api.lib.perm.auth import auth_abandoned
from api.models.acl import User, Role
from api.resource import APIView
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.acl.cache import RoleCache


class LoginView(APIView):
    url_prefix = "/login"

    @args_required("username")
    @args_required("password")
    @auth_abandoned
    def post(self):
        username = request.values.get("username") or request.values.get("email")
        password = request.values.get("password")
        if current_app.config.get('AUTH_WITH_LDAP'):
            user, authenticated = User.query.authenticate_with_ldap(username, password)
        else:
            user, authenticated = User.query.authenticate(username, password)
        if not user:
            return abort(403, "User <{0}> does not exist".format(username))
        if not authenticated:
            return abort(403, "invalid username or password")

        login_user(user)

        token = jwt.encode({
            'sub': user.email,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=24 * 60 * 7)},
            current_app.config['SECRET_KEY'])

        role = Role.get_by(uid=user.uid, first=True, to_dict=False)
        if role:
            parent_ids = RoleRelationCRUD.recursive_parent_ids(role.id)
            parent_roles = [RoleCache.get(i).name for i in parent_ids]
        else:
            parent_roles = []
        session["acl"] = dict(uid=user.uid,
                              avatar=user.avatar,
                              userName=user.username,
                              nickName=user.nickname,
                              parentRoles=parent_roles)

        return self.jsonify(token=token.decode())


class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)
