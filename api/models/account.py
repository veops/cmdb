# -*- coding:utf-8 -*-

import copy
import hashlib
from datetime import datetime

import six
from flask import current_app
from flask_sqlalchemy import BaseQuery

from api.extensions import db
from api.extensions import cache
from api.lib.database import CRUDModel


class UserQuery(BaseQuery):

    def authenticate(self, login, password):
        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).first()
        if user:
            current_app.logger.info(user)
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def authenticate_with_key(self, key, secret, args, path):
        user = self.filter(User.key == key).filter(User.block == 0).first()
        if not user:
            return None, False
        if user and hashlib.sha1('{0}{1}{2}'.format(
                path, user.secret, "".join(args)).encode("utf-8")).hexdigest() == secret:
            authenticated = True
        else:
            authenticated = False
        return user, authenticated

    def search(self, key):
        query = self.filter(db.or_(User.email == key,
                                   User.nickname.ilike('%' + key + '%'),
                                   User.username.ilike('%' + key + '%')))
        return query

    def get_by_username(self, username):
        user = self.filter(User.username == username).first()
        return user

    def get_by_nickname(self, nickname):
        user = self.filter(User.nickname == nickname).first()
        return user

    def get(self, uid):
        user = self.filter(User.uid == uid).first()
        return copy.deepcopy(user)


class User(CRUDModel):
    __tablename__ = 'users'
    __bind_key__ = "user"
    query_class = UserQuery

    ADMIN = 1
    OP = 2

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(20))
    catalog = db.Column(db.String(64))
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(14), unique=True)
    _password = db.Column("password", db.String(80))
    key = db.Column(db.String(32), nullable=False)
    secret = db.Column(db.String(32), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    block = db.Column(db.Boolean, default=False)
    has_logined = db.Column(db.Boolean, default=False)
    wx_id = db.Column(db.String(32))
    avatar = db.Column(db.String(128))

    def __str__(self):
        return self.username

    def is_active(self):
        return not self.block

    def get_id(self):
        return self.uid

    @staticmethod
    def is_authenticated():
        return True

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hashlib.md5(password.encode('utf-8')).hexdigest()

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == password

    @property
    def roles(self):
        urs = db.session.query(UserRole.rid).filter(
            UserRole.uid == self.uid).all()
        return [x.rid for x in urs]

    @property
    def rolenames(self):
        roles = list()
        for rid in self.roles:
            role = db.session.query(Role).filter(Role.rid == rid).first()
            roles.append(role.role_name)
        return roles

    @property
    def is_admin(self):
        return self.ADMIN in self.roles


class Role(CRUDModel):
    __tablename__ = 'roles'
    __bind_key__ = "user"

    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(64), nullable=False, unique=True)


class UserRole(CRUDModel):
    __tablename__ = 'users_roles'
    __bind_key__ = "user"

    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('roles.rid'), primary_key=True)


class UserCache(object):
    @classmethod
    def get(cls, key):
        user = cache.get("User::uid::%s" % key) or \
            cache.get("User::username::%s" % key) or \
            cache.get("User::nickname::%s" % key)
        if not user:
            user = User.query.get(key) or \
                User.query.get_by_username(key) or \
                User.query.get_by_nickname(key)
        if user:
            cls.set(user)
        return user

    @classmethod
    def set(cls, user):
        cache.set("User::uid::%s" % user.uid, user)
        cache.set("User::username::%s" % user.username, user)
        cache.set("User::nickname::%s" % user.nickname, user)

    @classmethod
    def clean(cls, user):
        cache.delete("User::uid::%s" % user.uid)
        cache.delete("User::username::%s" % user.username)
        cache.delete("User::nickname::%s" % user.nickname)


class RoleCache(object):
    @classmethod
    def get(cls, rid):
        role = None
        if isinstance(rid, six.integer_types):
            role = cache.get("Role::rid::%s" % rid)
            if not role:
                role = db.session.query(Role).filter(Role.rid == rid).first()
                cls.set(role)
        elif isinstance(rid, six.string_types):
            role = cache.get("Role::role_name::%s" % rid)
            if not role:
                role = db.session.query(Role).filter(
                    Role.role_name == rid).first()
                cls.set(role)
        return role

    @classmethod
    def set(cls, role):
        cache.set("Role::rid::%s" % role.rid, role)
        cache.set("Role::role_name::%s" % role.role_name, role)

    @classmethod
    def clean(cls, role):
        cache.delete("Role::rid::%s" % role.rid, role)
        cache.delete("Role::role_name::%s" % role.role_name, role)
