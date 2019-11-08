# -*- coding:utf-8 -*-

from api.extensions import db
from api.lib.database import Model


class App(Model):
    __tablename__ = "acl_apps"

    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    app_id = db.Column(db.Text)
    secret_key = db.Column(db.Text)


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
