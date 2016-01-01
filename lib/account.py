# -*- coding:utf-8 -*- 


import uuid
import random
import string
import datetime

from flask import current_app
from flask import abort

from extensions import db
from models.account import UserCache
from models.account import User
from models.account import UserRole


class AccountManager(object):
    def __init__(self):
        pass

    def get_user_by_uid(self, uid):
        user = UserCache.get(uid)
        return user

    def _generate_key(self):
        key = uuid.uuid4().hex
        secret = ''.join(random.sample(string.ascii_letters +
                                       string.digits + '~!@#$%^&*?', 32))
        return key, secret

    def validate(self, username, password):
        user, authenticated = User.query.authenticate(username, password)
        return user, authenticated

    def create_user(self, **kwargs):
        username = kwargs.get("username")
        if username:
            user = UserCache.get(username)
            if user is not None:
                user, authenticated = self.validate(
                    username, kwargs.get("password"))
                if authenticated:
                    return user
                else:
                    return abort(401, "authenticate validate failed")
        else:
            return abort(400, "argument username is required")
        user = User()
        email = kwargs.get("email", "")
        if not email:
            return abort(400, "argument email is required")
        user.email = email
        user.password = kwargs.get("password")
        user.username = kwargs.get("username", "")
        user.nickname = kwargs.get("nickname") if kwargs.get("nickname") \
            else kwargs.get("username", "")
        key, secret = self._generate_key()
        user.key = key
        user.secret = secret
        user.date_joined = datetime.datetime.now()
        user.block = 0

        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("create user is error {0}".format(str(e)))
            return abort(500, "create user is error, {0}".format(str(e)))
        return user

    def update_user(self, uid, **kwargs):
        user = UserCache.get(uid)
        if user is None:
            return abort(400, "the user[{0}] is not existed".format(uid))
        user.username = kwargs.get("username", "") \
            if kwargs.get("username") else user.username
        user.nickname = kwargs.get("nickname") \
            if kwargs.get("nickname") else user.nickname
        user.department = kwargs.get("department") \
            if kwargs.get("department") else user.department
        user.catalog = kwargs.get("catalog") \
            if kwargs.get("catalog") else user.catalog
        user.email = kwargs.get("email") \
            if kwargs.get("email") else user.email
        user.mobile = kwargs.get("mobile") \
            if kwargs.get("mobile") else user.mobile
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("create user is error {0}".format(str(e)))
            return abort(500, "create user is error, {0}".format(str(e)))
        return True, user

    def delete_user(self, uid):
        user = UserCache.get(uid)
        if user is None:
            return abort(400, "the user[{0}] is not existed".format(uid))
        db.session.query(UserRole).filter(UserRole.uid == uid).delete()
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("delete user error, {0}".format(str(e)))
            return abort(500, "delete user error, {0}".format(str(e)))
        return True, uid

    def update_password(self, uid, old, new, confirm):
        user = User.query.get(uid)
        if not user:
            return abort(400, "user is not existed")
        if not user.check_password(old):
            return abort(400, "invalidate old password")
        if not (new and confirm and new == confirm):
            return abort(400, """Password cannot be empty,
            two inputs must be the same""")
        user.password = new
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("set password error, %s" % str(e))
            return abort(500, "set password errors, {0:s}".format(str(e)))
        return True, user

    def reset_key(self, uid):
        user = UserCache.get(uid)
        if user is None:
            return abort(400, "the user[{0}] is not existed".format(uid))
        key, secret = self._generate_key()
        user.key = key
        user.secret = secret
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("reset key is error, {0}".format(str(e)))
            return abort(500, "reset key is error, {0}".format(str(e)))
        return True, user