# -*- coding:utf-8 -*-


import copy
import hashlib
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import BaseQuery

from api.extensions import db
from api.lib.database import CRUDModel
from api.lib.database import Model
from api.lib.database import SoftDeleteMixin


class App(Model):
    __tablename__ = "acl_apps"

    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    app_id = db.Column(db.Text)
    secret_key = db.Column(db.Text)


class UserQuery(BaseQuery):
    def _join(self, *args, **kwargs):
        super(UserQuery, self)._join(*args, **kwargs)

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


class User(CRUDModel, SoftDeleteMixin):
    __tablename__ = 'users'
    # __bind_key__ = "user"
    query_class = UserQuery

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

    password = db.synonym("_password", descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == password


class Role(Model):
    __tablename__ = "acl_roles"

    name = db.Column(db.Text, nullable=False)
    is_app_admin = db.Column(db.Boolean, default=False)
    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"))


class RoleRelation(Model):
    __tablename__ = "acl_role_relations"

    parent_id = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))

    __table_args__ = (
        db.UniqueConstraint("parent_id", "child_id", name="role_relation_unique"),)


class ResourceType(Model):
    __tablename__ = "acl_resource_types"

    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))


class ResourceGroup(Model):
    __tablename__ = "acl_resource_groups"

    name = db.Column(db.String(64), index=True, nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))

    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))

    __table_args__ = (db.UniqueConstraint("name", "resource_type_id", "app_id", name="resource_group_app_unique"),)


class Resource(Model):
    __tablename__ = "acl_resources"

    name = db.Column(db.String(128), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))

    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))

    __table_args__ = (db.UniqueConstraint("name", "resource_type_id", "app_id", name="resource_name_app_unique"),)


class ResourceGroupItems(Model):
    __tablename__ = "acl_resource_group_items"

    group_id = db.Column(db.Integer, db.ForeignKey('acl_resource_groups.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('acl_resources.id'), nullable=False)


class Permission(Model):
    __tablename__ = "acl_permissions"

    name = db.Column(db.String(64), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))

    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))

    __table_args__ = (db.UniqueConstraint("name", "resource_type_id", "app_id", name="perm_name_app_unique"),)


class RolePermission(Model):
    __tablename__ = "acl_role_permissions"

    rid = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('acl_resources.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('acl_resource_groups.id'))
    perm_id = db.Column(db.Integer, db.ForeignKey('acl_permissions.id'))

    perm = db.relationship("Permission", backref='acl_role_permissions.perm_id')
