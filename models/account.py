# -*- coding:utf-8 -*-


import hashlib
import copy
from datetime import datetime

from werkzeug.utils import cached_property
from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed
from flask.ext.principal import UserNeed
from flask.ext.principal import Permission

from extensions import db
from extensions import cache
from permissions import admin
from models import row2dict


class UserQuery(BaseQuery):
    def from_identity(self, identity):
        """
        Loads user from flask.ext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkey patched to the identity instance.

        If no user found then None is returned.
        """

        try:
            _id = identity.id
            if _id:
                _id = int(_id)
            user = self.get(_id)
        except ValueError:
            user = None
        except Exception:
            user = None
        if user:
            identity.provides.update(user.provides)
        identity.user = user
        return user

    def authenticate(self, login, password):
        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def authenticate_with_key(self, key, secret, args, path):
        user = self.filter(User.key == key).filter(User.block == 0).first()
        if not user:
            return None, False
        if user and hashlib.sha1('%s%s%s' % (
                path, user.secret, "".join(args))).hexdigest() == secret:
            authenticated = True
        else:
            authenticated = False
        return row2dict(user), authenticated

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

    def is_exits(self, username):
        user = self.filter(User.username == username).first()
        return user is not None


class User(db.Model):
    __tablename__ = 'users'
    query_class = UserQuery

    ADMIN = 1

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(20))
    catalog = db.Column(db.String(64))
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(14), unique=True)
    _password = db.Column("password", db.String(80), nullable=False)
    key = db.Column(db.String(32), nullable=False)
    secret = db.Column(db.String(32), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    block = db.Column(db.Boolean, default=False)
    has_logined = db.Column(db.Boolean, default=False)

    class Permissions(object):
        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def is_admin(self):
            return Permission(UserNeed(self.obj.id)) & admin

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = password

    password = db.synonym("_password", descriptor=property(
        _get_password, _set_password))

    def check_password(self, password):
        return self.password == password

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'), UserNeed(self.uid)]
        for r in self.rolenames:
            needs.append(RoleNeed(r))
        if self.is_admin:
            needs.append(RoleNeed('admin'))
        return needs

    @property
    def roles(self):
        urs = db.session.query(UserRole.rid).filter(
            UserRole.uid == self.uid).all()
        return [x.rid for x in urs]

    @property
    def rolenames(self):
        return [db.session.query(Role.role_name).filter(
            Role.rid == rid).first().role_name for rid in self.roles]

    @property
    def is_admin(self):
        return self.ADMIN in self.roles


class Role(db.Model):
    __tablename__ = 'roles'

    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(64), nullable=False, unique=True)


class UserRole(db.Model):
    __tablename__ = 'users_roles'

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
        if isinstance(rid, (int, long)):
            role = cache.get("Role::rid::%s" % rid)
            if not role:
                role = db.session.query(Role).filter(Role.rid == rid).first()
                cls.set(role)
        elif isinstance(rid, basestring):
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