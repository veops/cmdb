# -*- coding:utf-8 -*-

from api.extensions import db
from api.lib.database import Model, TimestampMixin, SoftDeleteMixin, CRUDMixin


class ModelWithoutPK(db.Model, TimestampMixin, SoftDeleteMixin, CRUDMixin):
    __table_args__ = {"extend_existing": True}
    __abstract__ = True


class Department(ModelWithoutPK):
    __tablename__ = 'common_department'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    department_name = db.Column(db.VARCHAR(255), default='')
    department_director_id = db.Column(
        db.Integer, default=0)
    department_parent_id = db.Column(db.Integer, default=1)

    sort_value = db.Column(db.Integer, default=0)

    acl_rid = db.Column(db.Integer, default=0)


class Employee(ModelWithoutPK):
    __tablename__ = 'common_employee'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.VARCHAR(255), default='')
    username = db.Column(db.VARCHAR(255), default='')
    nickname = db.Column(db.VARCHAR(255), default='')
    sex = db.Column(db.VARCHAR(64), default='')
    position_name = db.Column(db.VARCHAR(255), default='')
    mobile = db.Column(db.VARCHAR(255), default='')
    avatar = db.Column(db.VARCHAR(255), default='')

    direct_supervisor_id = db.Column(db.Integer, default=0)

    department_id = db.Column(db.Integer,
                              db.ForeignKey('common_department.department_id')
                              )

    acl_uid = db.Column(db.Integer, default=0)
    acl_rid = db.Column(db.Integer, default=0)
    acl_virtual_rid = db.Column(db.Integer, default=0)
    last_login = db.Column(db.TIMESTAMP, nullable=True)
    block = db.Column(db.Integer, default=0)

    notice_info = db.Column(db.JSON, default={})

    _department = db.relationship(
        'Department', backref='common_employee.department_id',
        lazy='joined'
    )


class EmployeeInfo(Model):
    __tablename__ = 'common_employee_info'

    info = db.Column(db.JSON, default={})
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'common_employee.employee_id'))
    employee = db.relationship(
        'Employee', backref='common_employee.employee_id', lazy='joined')


class CompanyInfo(Model):
    __tablename__ = "common_company_info_json"

    info = db.Column(db.JSON)


class InternalMessage(Model):
    __tablename__ = "common_internal_message"

    title = db.Column(db.VARCHAR(255), nullable=True)
    content = db.Column(db.TEXT, nullable=True)
    path = db.Column(db.VARCHAR(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    app_name = db.Column(db.VARCHAR(128), nullable=False)
    category = db.Column(db.VARCHAR(128), nullable=False)
    message_data = db.Column(db.JSON, nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('common_employee.employee_id'), comment='ID')


class CommonData(Model):
    __table_name__ = 'common_data'

    data_type = db.Column(db.VARCHAR(255), default='')
    data = db.Column(db.JSON)


class NoticeConfig(Model):
    __tablename__ = "common_notice_config"

    platform = db.Column(db.VARCHAR(255), nullable=False)
    info = db.Column(db.JSON)
