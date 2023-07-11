# -*- coding:utf-8 -*-

from api.extensions import db
from api.lib.database import Model, TimestampMixin, SoftDeleteMixin, CRUDMixin


class ModelWithoutPK(db.Model, TimestampMixin, SoftDeleteMixin, CRUDMixin):
    __table_args__ = {"extend_existing": True}
    __abstract__ = True


class Department(ModelWithoutPK):
    __tablename__ = 'common_department'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    department_name = db.Column(db.VARCHAR(255), default='', comment='部门名称')
    department_director_id = db.Column(
        db.Integer, default=0, comment='部门负责人ID')
    department_parent_id = db.Column(db.Integer, default=1, comment='上级部门ID')

    sort_value = db.Column(db.Integer, default=0, comment='排序值')

    acl_rid = db.Column(db.Integer, comment='ACL中rid', default=0)


class Employee(ModelWithoutPK):
    __tablename__ = 'common_employee'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.VARCHAR(255), default='', comment='邮箱')
    username = db.Column(db.VARCHAR(255), default='', comment='用户名')
    nickname = db.Column(db.VARCHAR(255), default='', comment='姓名')
    sex = db.Column(db.VARCHAR(64), default='', comment='性别')
    position_name = db.Column(db.VARCHAR(255), default='', comment='职位名称')
    mobile = db.Column(db.VARCHAR(255), default='', comment='电话号码')
    avatar = db.Column(db.VARCHAR(255), default='', comment='头像')

    direct_supervisor_id = db.Column(db.Integer, default=0, comment='直接上级ID')

    department_id = db.Column(db.Integer,
                              db.ForeignKey('common_department.department_id'),
                              comment='部门ID',
                              )

    acl_uid = db.Column(db.Integer, comment='ACL中uid', default=0)
    acl_rid = db.Column(db.Integer, comment='ACL中rid', default=0)
    acl_virtual_rid = db.Column(db.Integer, comment='ACL中虚拟角色rid', default=0)
    last_login = db.Column(db.TIMESTAMP, nullable=True, comment='上次登录时间')
    block = db.Column(db.Integer, comment='锁定状态', default=0)

    _department = db.relationship(
        'Department', backref='common_employee.department_id',
        lazy='joined'
    )


class EmployeeInfo(Model):
    """
    员工信息
    """
    __tablename__ = 'common_employee_info'

    info = db.Column(db.JSON, default={}, comment='员工信息')
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'common_employee.employee_id'), comment='员工ID')
    employee = db.relationship(
        'Employee', backref='common_employee.employee_id', lazy='joined')


class CompanyInfo(Model):
    __tablename__ = "common_company_info_json"

    info = db.Column(db.JSON)


class InternalMessage(Model):
    """
    内部消息
    """
    __tablename__ = "common_internal_message"

    title = db.Column(db.VARCHAR(255), nullable=True, comment='标题')
    content = db.Column(db.TEXT, nullable=True, comment='内容')
    path = db.Column(db.VARCHAR(255), nullable=True, comment='跳转路径')
    is_read = db.Column(db.Boolean, default=False, comment='是否已读')
    app_name = db.Column(db.VARCHAR(128), nullable=False, comment='应用名称')
    category = db.Column(db.VARCHAR(128), nullable=False, comment='分类')
    message_data = db.Column(db.JSON, nullable=True, comment='数据')
    employee_id = db.Column(db.Integer, db.ForeignKey('common_employee.employee_id'), comment='ID')
