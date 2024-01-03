# -*- coding:utf-8 -*-

from flask import abort, current_app
from treelib import Tree
from wtforms import Form
from wtforms import IntegerField
from wtforms import StringField
from wtforms import validators

from api.extensions import db
from api.lib.common_setting.resp_format import ErrFormat
from api.lib.common_setting.acl import ACLManager
from api.lib.perm.acl.role import RoleCRUD
from api.models.common_setting import Department, Employee

sub_departments_column_name = 'sub_departments'


def get_all_department_list(to_dict=True):
    criterion = [
        Department.deleted == 0,
    ]
    query = Department.query.filter(
        *criterion
    ).order_by(Department.department_id.asc())
    results = query.all()
    if to_dict:
        datas = []
        for r in results:
            d = r.to_dict()
            if r.department_id == 0:
                d['department_name'] = ErrFormat.company_wide
            datas.append(d)
        return datas
    return results


def get_all_employee_list(block=0, to_dict=True):
    criterion = [
        Employee.deleted == 0,
    ]
    if block >= 0:
        criterion.append(
            Employee.block == block
        )

    results = db.session.query(Employee).filter(*criterion).all()

    DepartmentTreeEmployeeColumns = [
        'acl_rid',
        'employee_id',
        'username',
        'nickname',
        'email',
        'mobile',
        'direct_supervisor_id',
        'block',
        'department_id',
    ]

    def format_columns(e):
        return {column: getattr(e, column) for column in DepartmentTreeEmployeeColumns}

    return [format_columns(r) for r in results] if to_dict else results


class DepartmentTree(object):
    def __init__(self, append_employee=False, block=-1):
        self.append_employee = append_employee
        self.block = block
        self.all_department_list = get_all_department_list()
        self.all_employee_list = get_all_employee_list(
            block) if append_employee else None

    def prepare(self):
        pass

    def get_employees_by_d_id(self, d_id):
        block = self.block

        def filter_department_id(e):
            if self.block != -1:
                return e['department_id'] == d_id and e['block'] == block
            return e.department_id == d_id

        results = list(filter(lambda e: filter_department_id(e), self.all_employee_list))

        return results

    def get_department_by_parent_id(self, parent_id):
        results = list(filter(lambda d: d['department_parent_id'] == parent_id, self.all_department_list))
        if not results:
            return []
        return results

    def get_tree_departments(self):
        # 一级部门
        top_departments = self.get_department_by_parent_id(-1)
        if len(top_departments) == 0:
            return []

        d_list = []

        for top_d in top_departments:
            department_id = top_d['department_id']
            sub_deps = self.get_department_by_parent_id(department_id)
            employees = []
            if self.append_employee:
                employees = self.get_employees_by_d_id(department_id)

            top_d['employees'] = employees
            top_d['department_name'] = ErrFormat.company_wide
            if len(sub_deps) == 0:
                top_d[sub_departments_column_name] = []
                d_list.append(top_d)
                continue

            self.parse_sub_department(sub_deps, top_d)
            d_list.append(top_d)

        return d_list

    def get_all_departments(self, is_tree=1):
        if len(self.all_department_list) == 0:
            return []

        if is_tree != 1:
            return self.all_department_list

        return self.get_tree_departments()

    def parse_sub_department(self, deps, top_d):
        sub_departments = []
        for d in deps:
            sub_deps = self.get_department_by_parent_id(d['department_id'])
            employees = []
            if self.append_employee:
                employees = self.get_employees_by_d_id(d['department_id'])

            d['employees'] = employees

            if len(sub_deps) == 0:
                d[sub_departments_column_name] = []
                sub_departments.append(d)
                continue

            self.parse_sub_department(sub_deps, d)
            sub_departments.append(d)

        top_d[sub_departments_column_name] = sub_departments


class DepartmentForm(Form):
    department_name = StringField(validators=[
        validators.DataRequired(message="部门名称不能为空"),
        validators.Length(max=255),
    ])

    department_director_id = IntegerField(validators=[], default=0)
    department_parent_id = IntegerField(validators=[], default=1)


class DepartmentCRUD(object):

    @staticmethod
    def get_department_by_id(d_id, to_dict=True):
        return Department.get_by(first=True, department_id=d_id, to_dict=to_dict)

    @staticmethod
    def add(**kwargs):
        DepartmentCRUD.check_department_name_unique(kwargs['department_name'])
        department_parent_id = kwargs.get('department_parent_id', 0)
        DepartmentCRUD.check_department_parent_id(department_parent_id)

        DepartmentCRUD.check_department_parent_id_allow(
            -1, department_parent_id)

        try:
            role = RoleCRUD.add_role(name=kwargs['department_name'])
        except Exception as e:
            return abort(400, ErrFormat.acl_add_role_failed.format(str(e)))

        kwargs['acl_rid'] = role.id
        try:
            db_department = Department.create(
                **kwargs
            )

        except Exception as e:
            return abort(400, str(e))

        return db_department

    @staticmethod
    def check_department_parent_id_allow(d_id, department_parent_id):
        if department_parent_id == 0:
            return
        allow_p_d_id_list = DepartmentCRUD.get_allow_parent_d_id_by(d_id)
        target = list(
            filter(lambda d: d['department_id'] == department_parent_id, allow_p_d_id_list))
        if len(target) == 0:
            try:
                dep = Department.get_by(
                    first=True, to_dict=False, department_id=department_parent_id)
                name = dep.department_name if dep else ErrFormat.department_id_not_found.format(department_parent_id)
            except Exception as e:
                current_app.logger.error(str(e))
                name = ErrFormat.department_id_not_found.format(department_parent_id)
            abort(400, ErrFormat.cannot_to_be_parent_department.format(name))

    @staticmethod
    def check_department_parent_id(department_parent_id):
        if int(department_parent_id) < 0:
            abort(400, ErrFormat.parent_department_id_must_more_than_zero)

    @staticmethod
    def check_department_name_unique(name, _id=0):
        criterion = [
            Department.department_name == name,
            Department.deleted == 0,
        ]
        if _id > 0:
            criterion.append(
                Department.department_id != _id
            )

        res = Department.query.filter(
            *criterion
        ).all()

        res and abort(
            400, ErrFormat.department_name_already_exists.format(name)
        )

    @staticmethod
    def edit(_id, **kwargs):
        DepartmentCRUD.check_department_name_unique(
            kwargs['department_name'], _id)
        kwargs.pop('department_id', None)
        existed = Department.get_by(
            first=True, department_id=_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.department_id_not_found.format(_id))

        department_parent_id = kwargs.get('department_parent_id', 0)
        DepartmentCRUD.check_department_parent_id(department_parent_id)
        if department_parent_id > 0:
            DepartmentCRUD.check_department_parent_id_allow(
                _id, department_parent_id)

        try:
            RoleCRUD.update_role(
                existed.acl_rid, name=kwargs['department_name'])
        except Exception as e:
            return abort(400, ErrFormat.acl_update_role_failed.format(str(e)))

        try:
            return existed.update(**kwargs)
        except Exception as e:
            return abort(400, str(e))

    @staticmethod
    def delete(_id):
        existed = Department.get_by(
            first=True, department_id=_id, to_dict=False)
        if not existed:
            abort(404, ErrFormat.department_id_not_found.format(_id))
        try:
            RoleCRUD.delete_role(existed.acl_rid)
        except Exception as e:
            current_app.logger.error(str(e))

        return existed.soft_delete()

    @staticmethod
    def get_allow_parent_d_id_by(department_id):
        tree_list = DepartmentCRUD.get_department_tree_list()

        allow_d_id_list = []

        for tree in tree_list:
            if department_id > 0:
                try:
                    tree.remove_subtree(department_id)
                except Exception as e:
                    current_app.logger.error(str(e))

            [allow_d_id_list.append({'department_id': int(n.identifier), 'department_name': n.tag}) for n in
             tree.all_nodes()]

        return allow_d_id_list

    @staticmethod
    def update_department_sort(department_list):
        d_map = {d['id']: d['sort_value'] for d in department_list}
        d_id = [d['id'] for d in department_list]

        db_list = Department.query.filter(
            Department.department_id.in_(d_id),
            Department.deleted == 0
        ).all()

        for existed in db_list:
            existed.update(sort_value=d_map[existed.department_id])

        return []

    @staticmethod
    def get_all_departments_with_employee(block):
        return DepartmentTree(True, block).get_all_departments(1)

    @staticmethod
    def get_department_tree_list():
        all_deps = get_all_department_list()
        if len(all_deps) == 0:
            return []

        top_deps = list(filter(lambda d: d['department_parent_id'] == -1, all_deps))
        if len(top_deps) == 0:
            return []

        tree_list = []

        for top_d in top_deps:
            top_d['department_name'] = ErrFormat.company_wide
            tree = Tree()
            identifier_root = top_d['department_id']
            tree.create_node(
                top_d['department_name'],
                identifier_root
            )
            sub_ds = list(filter(lambda d: d['department_parent_id'] == identifier_root, all_deps))
            if len(sub_ds) == 0:
                tree_list.append(tree)
                continue

            DepartmentCRUD.parse_sub_department_node(
                sub_ds, all_deps, tree, identifier_root)

            tree_list.append(tree)

        return tree_list

    @staticmethod
    def parse_sub_department_node(sub_ds, all_ds, tree, parent_id):
        for d in sub_ds:
            tree.create_node(
                d['department_name'],
                d['department_id'],
                parent=parent_id
            )

            next_sub_ds = list(filter(lambda item_d: item_d['department_parent_id'] == d['department_id'], all_ds))
            if len(next_sub_ds) == 0:
                continue

            DepartmentCRUD.parse_sub_department_node(
                next_sub_ds, all_ds, tree, d['department_id'])

    @staticmethod
    def get_department_by_query(query, to_dict=True):
        results = query.all()
        if not results:
            return []
        return results if not to_dict else [r.to_dict() for r in results]

    @staticmethod
    def get_departments_and_ids(department_parent_id, block):
        query = Department.query.filter(
            Department.department_parent_id == department_parent_id,
            Department.deleted == 0,
        ).order_by(Department.sort_value.asc())
        all_departments = DepartmentCRUD.get_department_by_query(query)
        if len(all_departments) == 0:
            return [], []

        tree_list = DepartmentCRUD.get_department_tree_list()
        all_employee_list = get_all_employee_list(block)

        department_id_list = [d['department_id'] for d in all_departments]
        query = Department.query.filter(
            Department.department_parent_id.in_(department_id_list),
            Department.deleted == 0,
        ).order_by(Department.sort_value.asc()).group_by(Department.department_id)
        sub_deps = DepartmentCRUD.get_department_by_query(query)

        sub_map = {d['department_parent_id']: 1 for d in sub_deps}

        for d in all_departments:
            d['has_sub'] = sub_map.get(d['department_id'], 0)

            d_ids = DepartmentCRUD.get_department_id_list_by_root(d['department_id'], tree_list)

            d['employee_count'] = len(list(filter(lambda e: e['department_id'] in d_ids, all_employee_list)))

            if int(department_parent_id) == -1:
                d['department_name'] = ErrFormat.company_wide

        return all_departments, department_id_list

    @staticmethod
    def get_department_id_list_by_root(root_department_id, tree_list=None):
        if tree_list is None:
            tree_list = DepartmentCRUD.get_department_tree_list()
        id_list = []
        for tree in tree_list:
            try:
                tmp_tree = tree.subtree(root_department_id)
                [id_list.append(int(n.identifier))
                 for n in tmp_tree.all_nodes()]
            except Exception as e:
                current_app.logger.error(str(e))

        return id_list


class EditDepartmentInACL(object):

    @staticmethod
    def add_department_to_acl(department_id, op_uid):
        db_department = DepartmentCRUD.get_department_by_id(department_id, to_dict=False)
        if not db_department:
            return

        from api.models.acl import Role
        role = Role.get_by(first=True, name=db_department.department_name, app_id=None)

        acl = ACLManager('acl', str(op_uid))
        if role is None:
            payload = {
                'app_id': 'acl',
                'name': db_department.department_name,
            }
            role = acl.create_role(payload)

        acl_rid = role.get('id') if role else 0

        db_department.update(
            acl_rid=acl_rid
        )
        info = f"add_department_to_acl, acl_rid: {acl_rid}"
        current_app.logger.info(info)
        return info

    @staticmethod
    def delete_department_from_acl(department_rids, op_uid):
        acl = ACLManager('acl', str(op_uid))

        result = []

        for rid in department_rids:
            try:
                acl.delete_role(rid)
            except Exception as e:
                result.append(f"delete_department_in_acl, rid: {rid}, error: {e}")
                continue

        return result

    @staticmethod
    def edit_department_name_in_acl(d_rid: int, d_name: str, op_uid: int):
        acl = ACLManager('acl', str(op_uid))
        payload = {
            'name': d_name
        }
        try:
            acl.edit_role(d_rid, payload)
        except Exception as e:
            return f"edit_department_name_in_acl, rid: {d_rid}, error: {e}"

        return f"edit_department_name_in_acl, rid: {d_rid}, success"

    @staticmethod
    def edit_employee_department_in_acl(e_list: list, new_d_id: int, op_uid: int):
        result = []
        new_department = DepartmentCRUD.get_department_by_id(new_d_id, False)
        if not new_department:
            result.append(f"{new_d_id} new_department is None")
            return result

        from api.models.acl import Role
        new_role = Role.get_by(first=True, name=new_department.department_name, app_id=None)
        new_d_rid_in_acl = new_role.get('id') if new_role else 0
        if new_d_rid_in_acl == 0:
            return

        if new_d_rid_in_acl != new_department.acl_rid:
            new_department.update(
                acl_rid=new_d_rid_in_acl
            )
        new_department_acl_rid = new_department.acl_rid if new_d_rid_in_acl == new_department.acl_rid else \
            new_d_rid_in_acl

        acl = ACLManager('acl', str(op_uid))
        for employee in e_list:
            old_department = DepartmentCRUD.get_department_by_id(employee.get('department_id'), False)
            if not old_department:
                continue
            employee_acl_rid = employee.get('e_acl_rid')
            if employee_acl_rid == 0:
                result.append(f"employee_acl_rid == 0")
                continue

            old_role = Role.get_by(first=True, name=old_department.department_name, app_id=None)
            old_d_rid_in_acl = old_role.get('id') if old_role else 0
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
                result.append(
                    f"remove_user_from_role employee_acl_rid: {employee_acl_rid}, parent_id: {d_acl_rid}, err: {e}")

            payload = {
                'app_id': 'acl',
                'child_ids': [employee_acl_rid],
            }
            try:
                acl.add_user_to_role(new_department_acl_rid, payload)
            except Exception as e:
                result.append(
                    f"add_user_to_role employee_acl_rid: {employee_acl_rid}, parent_id: {d_acl_rid}, err: {e}")

        return result
