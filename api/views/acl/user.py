# -*- coding:utf-8 -*-


from flask import request
from flask import session
from flask_login import current_user

from api.lib.decorator import args_required
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.acl.user import UserCRUD
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class GetUserInfoView(APIView):
    url_prefix = "/users/info"

    def get(self):
        name = session.get("acl", {}).get("nickName") or session.get("CAS_USERNAME") or current_user.nickname
        role = dict(permissions=session.get("acl", {}).get("parentRoles", []) or ["admin"])
        avatar = session.get("acl", {}).get("avatar") or current_user.avatar
        return self.jsonify(result=dict(name=name,
                                        role=role,
                                        avatar=avatar))


class UserView(APIView):
    url_prefix = ("/users", "/users/<int:uid>")

    def get(self):
        page = get_page(request.values.get('page', 1))
        page_size = get_page_size(request.values.get('page_size'))
        q = request.values.get("q")
        numfound, users = UserCRUD.search(q, page, page_size)

        id2parents = RoleRelationCRUD.get_parents(uids=[i.uid for i in users])

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
    def post(self):
        user = UserCRUD.add(**request.values)

        return self.jsonify(user.to_dict())

    def put(self, uid):
        user = UserCRUD.update(uid, **request.values)

        return self.jsonify(user.to_dict())

    def delete(self, uid):
        UserCRUD.delete(uid)

        return self.jsonify(uid=uid)


class UserResetKeySecretView(APIView):
    url_prefix = "/users/reset_key_secret"

    def post(self):
        key, secret = UserCRUD.reset_key_secret()

        return self.jsonify(key=key, secret=secret)

    def put(self):
        return self.post()
