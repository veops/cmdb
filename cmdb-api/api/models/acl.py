# -*- coding:utf-8 -*-


import copy
import hashlib
from datetime import datetime

from flask import current_app
from flask import session
from flask_sqlalchemy import BaseQuery

from api.extensions import db
from api.lib.database import CRUDModel
from api.lib.database import Model
from api.lib.database import Model2
from api.lib.database import SoftDeleteMixin
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.perm.acl.const import OperateType
from api.lib.perm.acl.resp_format import ErrFormat


class App(Model):
    __tablename__ = "acl_apps"

    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    app_id = db.Column(db.Text)
    secret_key = db.Column(db.Text)


class UserQuery(BaseQuery):

    def authenticate(self, login, password):
        from api.lib.perm.acl.audit import AuditCRUD

        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).filter(User.deleted.is_(False)).filter(User.block == 0).first()
        if user:
            authenticated = user.check_password(password)
            if authenticated:
                _id = AuditCRUD.add_login_log(login, True, ErrFormat.login_succeed)
                session['LOGIN_ID'] = _id
            else:
                AuditCRUD.add_login_log(login, False, ErrFormat.invalid_password)
        else:
            authenticated = False

            AuditCRUD.add_login_log(login, False, ErrFormat.user_not_found.format(login))

        current_app.logger.info(("login", login, user, authenticated))

        return user, authenticated

    def authenticate_with_key(self, key, secret, args, path):
        user = self.filter(User.key == key).filter(User.deleted.is_(False)).filter(User.block == 0).first()
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

    def get_by_wxid(self, wx_id):
        user = self.filter(User.wx_id == wx_id).first()

        return user

    def get(self, uid):
        user = self.filter(User.uid == uid).first()

        return copy.deepcopy(user)


class User(CRUDModel, SoftDeleteMixin):
    __tablename__ = 'users'
    __bind_key__ = "user"
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
    employee_id = db.Column(db.String(16), index=True)
    avatar = db.Column(db.String(128))

    # apps = db.Column(db.JSON)

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
        return self.password == password or self.password == hashlib.md5(password.encode('utf-8')).hexdigest()


class RoleQuery(BaseQuery):

    def authenticate(self, login, password):
        role = self.filter(Role.name == login).filter(Role.deleted.is_(False)).first()
        if role:
            authenticated = role.check_password(password)

            if authenticated:
                from api.tasks.acl import op_record
                op_record.apply_async(args=(None, login, OperateType.LOGIN, ["ACL"]), queue=ACL_QUEUE)

        else:
            authenticated = False

        return role, authenticated

    def authenticate_with_key(self, key, secret, args, path):
        role = self.filter(Role.key == key).filter(Role.deleted.is_(False)).first()
        if not role:
            return None, False
        if role and hashlib.sha1('{0}{1}{2}'.format(
                path, role.secret, "".join(args)).encode("utf-8")).hexdigest() == secret:
            authenticated = True
        else:
            authenticated = False

        return role, authenticated


class Role(Model):
    __tablename__ = "acl_roles"
    query_class = RoleQuery

    name = db.Column(db.String(64), index=True, nullable=False)
    is_app_admin = db.Column(db.Boolean, default=False)
    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))
    uid = db.Column(db.Integer)
    _password = db.Column("password", db.String(80))
    key = db.Column(db.String(32))
    secret = db.Column(db.String(32))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            self._password = hashlib.md5(password.encode('utf-8')).hexdigest()

    password = db.synonym("_password", descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == password or self.password == hashlib.md5(password.encode('utf-8')).hexdigest()


class RoleRelation(Model):
    __tablename__ = "acl_role_relations"

    parent_id = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))
    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))


class ResourceType(Model):
    __tablename__ = "acl_resource_types"

    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))


class ResourceGroup(Model):
    __tablename__ = "acl_resource_groups"

    name = db.Column(db.String(64), index=True, nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))
    uid = db.Column(db.Integer, index=True)

    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))

    resource_type = db.relationship("ResourceType", backref='acl_resource_groups.resource_type_id')


class Resource(Model):
    __tablename__ = "acl_resources"

    name = db.Column(db.String(128), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))
    uid = db.Column(db.Integer, index=True)

    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))

    resource_type = db.relationship("ResourceType", backref='acl_resources.resource_type_id')


class ResourceGroupItems(Model):
    __tablename__ = "acl_resource_group_items"

    group_id = db.Column(db.Integer, db.ForeignKey('acl_resource_groups.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('acl_resources.id'), nullable=False)

    resource = db.relationship("Resource", backref='acl_resource_group_items.resource_id')


class Permission(Model):
    __tablename__ = "acl_permissions"

    name = db.Column(db.String(64), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey("acl_resource_types.id"))

    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))


class RolePermission(Model):
    __tablename__ = "acl_role_permissions"

    rid = db.Column(db.Integer, db.ForeignKey('acl_roles.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('acl_resources.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('acl_resource_groups.id'))
    perm_id = db.Column(db.Integer, db.ForeignKey('acl_permissions.id'))
    app_id = db.Column(db.Integer, db.ForeignKey("acl_apps.id"))

    perm = db.relationship("Permission", backref='acl_role_permissions.perm_id')


class Trigger(Model):
    __tablename__ = "acl_triggers"

    name = db.Column(db.String(128))
    wildcard = db.Column(db.Text)
    uid = db.Column(db.Text)  # TODO
    resource_type_id = db.Column(db.Integer, db.ForeignKey('acl_resource_types.id'))
    roles = db.Column(db.Text)  # TODO
    permissions = db.Column(db.Text)  # TODO
    enabled = db.Column(db.Boolean, default=True)

    app_id = db.Column(db.Integer, db.ForeignKey('acl_apps.id'))


class OperationRecord(Model):
    __tablename__ = "acl_operation_records"

    app = db.Column(db.String(32), index=True)
    rolename = db.Column(db.String(32), index=True)
    operate = db.Column(db.Enum(*OperateType.all()), nullable=False)
    obj = db.Column(db.JSON)


class AuditRoleLog(Model):
    __tablename__ = "acl_audit_role_logs"

    app_id = db.Column(db.Integer, index=True)

    operate_uid = db.Column(db.Integer, comment='操作人uid', index=True)
    operate_type = db.Column(db.String(32), comment='操作类型', index=True)
    scope = db.Column(db.String(16), comment='范围')
    link_id = db.Column(db.Integer, comment='资源id', index=True)
    origin = db.Column(db.JSON, default=dict(), comment='原始数据')
    current = db.Column(db.JSON, default=dict(), comment='当前数据')
    extra = db.Column(db.JSON, default=dict(), comment='其他内容')
    source = db.Column(db.String(16), default='', comment='来源')


class AuditResourceLog(Model):
    __tablename__ = "acl_audit_resource_logs"

    app_id = db.Column(db.Integer, index=True)
    operate_uid = db.Column(db.Integer, comment='操作人uid', index=True)
    operate_type = db.Column(db.String(16), comment='操作类型', index=True)

    scope = db.Column(db.String(16), comment='范围')
    link_id = db.Column(db.Integer, comment='资源名', index=True)
    origin = db.Column(db.JSON, default=dict(), comment='原始数据')
    current = db.Column(db.JSON, default=dict(), comment='当前数据')
    extra = db.Column(db.JSON, default=dict(), comment='权限名')
    source = db.Column(db.String(16), default='', comment='来源')


class AuditPermissionLog(Model):
    __tablename__ = "acl_audit_permission_logs"

    app_id = db.Column(db.Integer, index=True)

    operate_uid = db.Column(db.Integer, comment='操作人uid', index=True)
    operate_type = db.Column(db.String(16), comment='操作类型', index=True)

    rid = db.Column(db.Integer, comment='角色id', index=True)
    resource_type_id = db.Column(db.Integer, comment='资源类型id', index=True)
    resource_ids = db.Column(db.JSON, default=[], comment='资源')
    group_ids = db.Column(db.JSON, default=[], comment='资源组')
    permission_ids = db.Column(db.JSON, default=[], comment='权限')
    source = db.Column(db.String(16), comment='来源')


class AuditTriggerLog(Model):
    __tablename__ = "acl_audit_trigger_logs"

    app_id = db.Column(db.Integer, index=True)

    trigger_id = db.Column(db.Integer, comment='trigger', index=True)
    operate_uid = db.Column(db.Integer, comment='操作人uid', index=True)
    operate_type = db.Column(db.String(16), comment='操作类型', index=True)

    origin = db.Column(db.JSON, default=dict(), comment='原始数据')
    current = db.Column(db.JSON, default=dict(), comment='当前数据')
    extra = db.Column(db.JSON, default=dict(), comment='权限名')
    source = db.Column(db.String(16), default='', comment='来源')


class AuditLoginLog(Model2):
    __tablename__ = "acl_audit_login_logs"

    username = db.Column(db.String(64), index=True)
    channel = db.Column(db.Enum('web', 'api', 'ssh'), default="web")
    ip = db.Column(db.String(15))
    browser = db.Column(db.String(256))
    description = db.Column(db.String(128))
    is_ok = db.Column(db.Boolean)
    login_at = db.Column(db.DateTime)
    logout_at = db.Column(db.DateTime)
