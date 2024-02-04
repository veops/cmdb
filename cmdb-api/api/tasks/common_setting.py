# -*- coding:utf-8 -*-
from flask import current_app

from api.extensions import celery
from api.lib.common_setting.acl import ACLManager
from api.lib.perm.acl.const import ACL_QUEUE
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import Department, Employee
from api.lib.decorator import flush_db
from api.lib.decorator import reconnect_db


@celery.task(name="common_setting.edit_employee_department_in_acl", queue=ACL_QUEUE)
@flush_db
@reconnect_db
def edit_employee_department_in_acl(e_list, new_d_id, op_uid):
    """
    :param e_list:{acl_rid: 11, department_id: 22}
    :param new_d_id
    :param op_uid
    """
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
        payload = {
            'app_id': 'acl',
            'parent_id': d_acl_rid,
        }
        try:
            acl.remove_user_from_role(employee_acl_rid, payload)
        except Exception as e:
            result.append(ErrFormat.acl_remove_user_from_role_failed.format(str(e)))

        payload = {
            'app_id': 'acl',
            'child_ids': [employee_acl_rid],
        }
        try:
            acl.add_user_to_role(new_department_acl_rid, payload)
        except Exception as e:
            result.append(ErrFormat.acl_add_user_to_role_failed.format(str(e)))

    return result


@celery.task(name="common_setting.refresh_employee_acl_info", queue=ACL_QUEUE)
@flush_db
@reconnect_db
def refresh_employee_acl_info(current_employee_id=None):
    acl = ACLManager('acl')
    role_map = {role['name']: role for role in acl.get_all_roles()}

    criterion = [
        Employee.deleted == 0
    ]
    query = Employee.query.filter(*criterion).order_by(
        Employee.created_at.desc()
    )
    current_employee_rid = 0

    for em in query.all():
        if current_employee_id and em.employee_id == current_employee_id:
            current_employee_rid = em.acl_rid if em.acl_rid else 0

        if em.acl_uid and em.acl_rid:
            continue
        role = role_map.get(em.username, None)
        if not role:
            continue

        params = dict()
        if not em.acl_uid:
            params['acl_uid'] = role.get('uid', 0)

        if not em.acl_rid:
            params['acl_rid'] = role.get('id', 0)

        if current_employee_id and em.employee_id == current_employee_id:
            current_employee_rid = params['acl_rid'] if params.get('acl_rid', 0) else 0

        try:
            em.update(**params)
            current_app.logger.info(
                f"refresh_employee_acl_info success, employee_id: {em.employee_id}, uid: {em.acl_uid}, "
                f"rid: {em.acl_rid}")
        except Exception as e:
            current_app.logger.error(str(e))
            continue

    if current_employee_rid and current_employee_rid > 0:
        try:
            from api.lib.common_setting.employee import GrantEmployeeACLPerm

            GrantEmployeeACLPerm().grant_by_rid(current_employee_rid, False)
            current_app.logger.info(f"GrantEmployeeACLPerm success, current_employee_rid: {current_employee_rid}")
        except Exception as e:
            current_app.logger.error(str(e))
