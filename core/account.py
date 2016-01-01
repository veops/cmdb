# -*- coding:utf-8 -*-


from flask import Blueprint
from flask import request

from flask import g
from flask import abort
from flask import jsonify

from models import row2dict
from lib.account import AccountManager
from lib.auth import auth_with_key


account = Blueprint('account', __name__)


@account.route("/<int:uid>", methods=["GET"])
@auth_with_key
def get_user(uid=None):
    manager = AccountManager()
    user = manager.get_user_by_uid(uid)
    if user:
        return jsonify(rolenames=user.rolenames, user=row2dict(user))
    else:
        return jsonify(user=None)


@account.route("", methods=["POST"])
@auth_with_key
def create_user():
    manager = AccountManager()
    params = {}
    for k, v in request.values.iteritems():
        params[k] = v
    user = manager.create_user(**params)
    return jsonify(user=row2dict(user))


@account.route("/<int:uid>", methods=["PUT"])
@auth_with_key
def update_user(uid=None):
    manager = AccountManager()
    params = {}
    for k, v in request.values.iteritems():
        params[k] = v
    ret, res = manager.update_user(uid, **params)
    if not ret:
        abort(res[0], res[1])
    return jsonify(user=row2dict(res), rolenames=res.rolenames)


@account.route("/<int:uid>", methods=["DELETE"])
@auth_with_key
def delete_user(uid=None):
    manager = AccountManager()
    ret, res = manager.delete_user(uid)
    if not ret:
        abort(res[0], res[1])
    return jsonify(uid=uid)


@account.route("/validate", methods=["POST"])
@auth_with_key
def validate():
    username = request.values.get("username")
    password = request.values.get("password")
    manager = AccountManager()
    user, authenticated = manager.validate(username, password)
    if user and not authenticated:
        return jsonify(code=401, user=row2dict(user), rolenames=user.rolenames)
    elif not user:
        return jsonify(code=404, message="user is not existed")
    return jsonify(code=200, user=row2dict(user), rolenames=user.rolenames)


@account.route("/key", methods=["PUT"])
@auth_with_key
def update_key():
    manager = AccountManager()
    ret, res = manager.reset_key(g.user.uid)
    if not ret:
        abort(res[0], res[1])
    return jsonify(user=row2dict(res), rolenames=res.rolenames)


@account.route("/password", methods=["PUT"])
@auth_with_key
def update_password():
    manager = AccountManager()
    old = request.values.get("password")
    new = request.values.get("new_password")
    confirm = request.values.get("confirm")
    ret, res = manager.update_password(g.user.uid, old, new, confirm)
    if not ret:
        abort(res[0], res[1])
    return jsonify(user=row2dict(res), rolenames=res.rolenames)
