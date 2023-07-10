# -*- coding:utf-8 -*-
import requests
from flask import current_app

from api.extensions import celery
from api.extensions import db
from api.lib.common_setting.acl import ACLManager
from api.lib.common_setting.const import COMMON_SETTING_QUEUE
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import Department


@celery.task(name="common_setting.edit_employee_department_in_acl", queue=COMMON_SETTING_QUEUE)
def edit_employee_department_in_acl(e_list, new_d_id, op_uid):
    """
    在 ACL 员工更换部门
    :param e_list: 员工列表 {acl_rid: 11, department_id: 22}
    :param new_d_id: 新部门 ID
    :param op_uid: 操作人 ID

    在老部门中删除员工
    在新部门中添加员工
    """
    db.session.remove()

    result = []
    new_department = Department.get_by(
        first=True, department_id=new_d_id, to_dict=False)
    if not new_department:
        result.append(ErrFormat.new_department_is_none)
        return result

    acl = ACLManager('acl', str(op_uid))
    role_map = {role['name']: role['id'] for role in acl.get_all_roles()}
    new_d_rid_in_acl = role_map.get(new_department.department_name, 0)
    if new_d_rid_in_acl == 0:
        return

    if new_d_rid_in_acl != new_department.acl_rid:
        new_department.update(
            acl_rid=new_d_rid_in_acl
        )
    new_department_acl_rid = new_department.acl_rid if new_d_rid_in_acl == new_department.acl_rid else new_d_rid_in_acl

    for employee in e_list:
        # 根据 部门ID获取部门 acl_rid
        old_department = Department.get_by(
            first=True, department_id=employee.get('department_id'), to_dict=False)
        if not old_department:
            continue
        employee_acl_rid = employee.get('e_acl_rid')
        if employee_acl_rid == 0:
            result.append(ErrFormat.employee_acl_rid_is_zero)
            continue

        old_d_rid_in_acl = role_map.get(old_department.department_name, 0)
        if old_d_rid_in_acl == 0:
            return
        if old_d_rid_in_acl != old_department.acl_rid:
            old_department.update(
                acl_rid=old_d_rid_in_acl
            )
        d_acl_rid = old_department.acl_rid if old_d_rid_in_acl == old_department.acl_rid else old_d_rid_in_acl
        # 在老部门中删除员工
        payload = {
            'app_id': 'acl',
            'parent_id': d_acl_rid,
        }
        try:
            acl.remove_user_from_role(employee_acl_rid, payload)
        except Exception as e:
            result.append(ErrFormat.acl_remove_user_from_role_failed.format(str(e)))

        # 在新部门中添加员工
        payload = {
            'app_id': 'acl',
            'child_ids': [employee_acl_rid],
        }
        try:
            acl.add_user_to_role(new_department_acl_rid, payload)
        except Exception as e:
            result.append(ErrFormat.acl_add_user_to_role_failed.format(str(e)))

    return result
