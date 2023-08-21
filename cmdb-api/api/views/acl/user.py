# -*- coding:utf-8 -*-


import requests
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import current_user

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import role_required
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.acl.user import UserCRUD
from api.lib.perm.auth import auth_with_app_token
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class GetUserInfoView(APIView):
    url_prefix = "/users/info"

    @auth_with_app_token
    def get(self):
        app_id = request.values.get('app_id')
        if not app_id:
            name = session.get("acl", {}).get("userName") or session.get("CAS_USERNAME") or \
                   current_user.username or request.values.get('username')
        else:

            name = request.values.get('username')

        current_app.logger.info("get user info for1: app_id: {0}, name: {1}".format(request.values.get('app_id'), name))
        user_info = ACLManager().get_user_info(name, request.values.get('app_id'))
        current_app.logger.info("get user info for2: {}".format(user_info))

        result = dict(name=user_info.get('nickname') or name,
                      username=user_info.get('username') or name,
                      email=user_info.get('email'),
                      uid=user_info.get('uid'),
                      rid=user_info.get('rid'),
                      role=dict(permissions=user_info.get('parents')),
                      avatar=user_info.get('avatar'))

        current_app.logger.info("get user info for3: {}".format(result))
        return self.jsonify(result=result)


class GetUserKeySecretView(APIView):
    url_prefix = "/users/secret"

    @auth_with_app_token
    def get(self):
        if not request.values.get('app_id'):
            name = session.get("acl", {}).get("userName") or session.get("CAS_USERNAME") or current_user.username
        else:
            name = request.values.get('username')

        user = UserCache.get(name) or abort(404, ErrFormat.user_not_found.format(name))

        return self.jsonify(key=user.key, secret=user.secret)


class UserView(APIView):
    url_prefix = ("/users", "/users/<int:uid>")

    @auth_with_app_token
    def get(self):
        page = get_page(request.values.get('page', 1))
        page_size = get_page_size(request.values.get('page_size'))
        q = request.values.get("q")
        numfound, users = UserCRUD.search(q, page, page_size)
        id2parents = RoleRelationCRUD.get_parents(uids=[i.uid for i in users], all_app=True)

        users = [i.to_dict() for i in users]
        for u in users:
            u.pop('password', None)
            u.pop('key', None)
            u.pop('secret', None)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            id2parents=id2parents,
                            users=users)

    @args_required('username')
    @args_required('email')
    @role_required("acl_admin")
    @args_validate(UserCRUD.cls)
    def post(self):
        request.values.pop('_key', None)
        request.values.pop('_secret', None)

        user = UserCRUD.add(**request.values)

        return self.jsonify(user.to_dict())

    @role_required("acl_admin")
    @args_validate(UserCRUD.cls)
    def put(self, uid):
        request.values.pop('_key', None)
        request.values.pop('_secret', None)

        user = UserCRUD.update(uid, **request.values)

        return self.jsonify(user.to_dict())

    @role_required("acl_admin")
    def delete(self, uid):
        if current_user.uid == uid:
            return abort(400, ErrFormat.invalid_operation)
        UserCRUD.delete(uid)

        return self.jsonify(uid=uid)


class UserOnTheJobView(APIView):
    url_prefix = ("/users/employee",)

    @auth_with_app_token
    def get(self):
        if current_app.config.get('HR_URI'):
            try:
                return self.jsonify(requests.get(current_app.config["HR_URI"]).json())
            except:
                return abort(400, ErrFormat.invalid_request)
        else:
            return self.jsonify(UserCRUD.get_employees())


class UserResetKeySecretView(APIView):
    url_prefix = "/users/reset_key_secret"

    def post(self):
        key, secret = UserCRUD.reset_key_secret()

        return self.jsonify(key=key, secret=secret)

    def put(self):
        return self.post()


class UserResetPasswordView(APIView):
    url_prefix = "/users/reset_password"

    @auth_with_app_token
    @args_required('username')
    @args_required('password')
    @args_validate(UserCRUD.cls, exclude_args=['app_id'])
    def post(self):
        if request.values.get('app_id'):
            app = AppCache.get(request.values['app_id'])
            if app.name not in ('cas-server', 'acl'):
                return abort(403, ErrFormat.invalid_request)

        elif hasattr(current_user, 'username'):
            if current_user.username != request.values['username']:
                return abort(403, ErrFormat.invalid_request)

        else:
            return abort(400, ErrFormat.invalid_operation)

        user = UserCache.get(request.values['username'])
        user or abort(404, ErrFormat.user_not_found.format(request.values['username']))

        UserCRUD.update(user.uid, password=request.values['password'])

        return self.jsonify(code=200)
