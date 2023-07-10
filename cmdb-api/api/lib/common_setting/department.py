# -*- coding:utf-8 -*-

from flask import abort
from treelib import Tree
from wtforms import Form
from wtforms import IntegerField
from wtforms import StringField
from wtforms import validators

from api.lib.common_setting.resp_format import ErrFormat
from api.lib.common_setting.utils import get_df_from_read_sql
from api.lib.perm.acl.role import RoleCRUD
from api.models.common_setting import Department, Employee

sub_departments_column_name = 'sub_departments'


def drop_ts_column(df):
    columns = list(df.columns)
    remove_columns = []
    for column in ['created_at', 'updated_at', 'deleted_at', 'last_login']:
        targets = list(filter(lambda c: c.startswith(column), columns))
        if targets:
            remove_columns.extend(targets)

    remove_columns = list(set(remove_columns))

    return df.drop(remove_columns, axis=1) if len(remove_columns) > 0 else df


def get_department_df():
    criterion = [
        Department.deleted == 0,
    ]
    query = Department.query.filter(
        *criterion
    )
    df = get_df_from_read_sql(query)
    if df.empty:
        return
    return drop_ts_column(df)


def get_all_employee_df(block=0):
    criterion = [
        Employee.deleted == 0,
    ]
    if block >= 0:
        criterion.append(
            Employee.block == block
        )

    entities = [getattr(Employee, c) for c in Employee.get_columns(
    ).keys() if c not in ['deleted', 'deleted_at']]
    query = Employee.query.with_entities(
        *entities
    ).filter(
        *criterion
    )
    df = get_df_from_read_sql(query)
    if df.empty:
        return df
    return drop_ts_column(df)


class DepartmentTree(object):
    def __init__(self, append_employee=False, block=-1):
        self.append_employee = append_employee
        self.block = block
        self.d_df = get_department_df()
        self.employee_df = get_all_employee_df(
            block) if append_employee else None

    def prepare(self):
        pass

    def get_employees_by_d_id(self, d_id):
        _df = self.employee_df[
            self.employee_df['department_id'].eq(d_id)
        ].sort_values(by=['direct_supervisor_id'], ascending=True)
        if _df.empty:
            return []

        if self.block != -1:
            _df = _df[
                _df['block'].eq(self.block)
            ]

        return _df.to_dict('records')

    def get_tree_departments(self):
        # 一级部门
        top_df = self.d_df[self.d_df['department_parent_id'].eq(-1)]
        if top_df.empty:
            return []

        d_list = []

        for index in top_df.index:
            top_d = top_df.loc[index].to_dict()

            department_id = top_d['department_id']

            # 检查 department_id 是否作为其他部门的 parent
            sub_df = self.d_df[
                self.d_df['department_parent_id'].eq(department_id)
            ].sort_values(by=['sort_value'], ascending=True)

            employees = []

            if self.append_employee:
                # 要包含员工
                employees = self.get_employees_by_d_id(department_id)

            top_d['employees'] = employees

            if sub_df.empty:
                top_d[sub_departments_column_name] = []
                d_list.append(top_d)
                continue

            self.parse_sub_department(sub_df, top_d)
            d_list.append(top_d)

        return d_list

    def get_all_departments(self, is_tree=1):
        if self.d_df.empty:
            return []

        if is_tree != 1:
            return self.d_df.to_dict('records')

        return self.get_tree_departments()

    def parse_sub_department(self, df, top_d):
        sub_departments = []
        for s_index in df.index:
            d = df.loc[s_index].to_dict()
            sub_df = self.d_df[
                self.d_df['department_parent_id'].eq(
                    df.at[s_index, 'department_id'])
            ].sort_values(by=['sort_value'], ascending=True)
            employees = []

            if self.append_employee:
                # 要包含员工
                employees = self.get_employees_by_d_id(
                    df.at[s_index, 'department_id'])

            d['employees'] = employees

            if sub_df.empty:
                d[sub_departments_column_name] = []
                sub_departments.append(d)
                continue

            self.parse_sub_department(sub_df, d)
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
        # 检查 department_parent_id 是否在许可范围内
        allow_p_d_id_list = DepartmentCRUD.get_allow_parent_d_id_by(d_id)
        target = list(
            filter(lambda d: d['department_id'] == department_parent_id, allow_p_d_id_list))
        if len(target) == 0:
            try:
                d = Department.get_by(
                    first=True, to_dict=False, department_id=department_parent_id)
                name = d.department_name if d else ErrFormat.department_id_not_found.format(department_parent_id)
            except Exception as e:
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
            existed.update(**kwargs)
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
            pass

        return existed.soft_delete()

    @staticmethod
    def get_allow_parent_d_id_by(department_id):
        """
        获取可以成为 department_id 的 department_parent_id 的 list
        """
        tree_list = DepartmentCRUD.get_department_tree_list()

        allow_d_id_list = []

        for tree in tree_list:
            if department_id > 0:
                try:
                    tree.remove_subtree(department_id)
                except Exception as e:
                    pass

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
        df = get_department_df()
        if df.empty:
            return []

        # 一级部门
        top_df = df[df['department_parent_id'].eq(-1)]
        if top_df.empty:
            return []

        tree_list = []

        for index in top_df.index:
            tree = Tree()
            identifier_root = top_df.at[index, 'department_id']
            tree.create_node(
                top_df.at[index, 'department_name'],
                identifier_root
            )

            # 检查 department_id 是否作为其他部门的 parent
            sub_df = df[
                df['department_parent_id'].eq(identifier_root)
            ]
            if sub_df.empty:
                tree_list.append(tree)
                continue

            DepartmentCRUD.parse_sub_department_node(
                sub_df, df, tree, identifier_root)

            tree_list.append(tree)

        return tree_list

    @staticmethod
    def parse_sub_department_node(df, all_df, tree, parent_id):
        for s_index in df.index:
            tree.create_node(
                df.at[s_index, 'department_name'],
                df.at[s_index, 'department_id'],
                parent=parent_id
            )

            sub_df = all_df[
                all_df['department_parent_id'].eq(
                    df.at[s_index, 'department_id'])
            ]
            if sub_df.empty:
                continue

            DepartmentCRUD.parse_sub_department_node(
                sub_df, all_df, tree, df.at[s_index, 'department_id'])

    @staticmethod
    def get_departments_and_ids(department_parent_id, block):
        query = Department.query.filter(
            Department.department_parent_id == department_parent_id,
            Department.deleted == 0,
        ).order_by(Department.sort_value.asc())
        df = get_df_from_read_sql(query)
        if df.empty:
            return [], []

        tree_list = DepartmentCRUD.get_department_tree_list()
        employee_df = get_all_employee_df(block)

        department_id_list = list(df['department_id'].values)
        query = Department.query.filter(
            Department.department_parent_id.in_(department_id_list),
            Department.deleted == 0,
        ).order_by(Department.sort_value.asc()).group_by(Department.department_id)
        sub_df = get_df_from_read_sql(query)
        if sub_df.empty:
            df['has_sub'] = 0

            def handle_row_employee_count(row):
                return len(employee_df[employee_df['department_id'] == row['department_id']])

            df['employee_count'] = df.apply(
                lambda row: handle_row_employee_count(row), axis=1)

        else:
            sub_map = {d['department_parent_id']: 1 for d in sub_df.to_dict('records')}

            def handle_row(row):
                d_ids = DepartmentCRUD.get_department_id_list_by_root(
                    row['department_id'], tree_list)
                row['employee_count'] = len(
                    employee_df[employee_df['department_id'].isin(d_ids)])

                row['has_sub'] = sub_map.get(row['department_id'], 0)

                return row

            df = df.apply(lambda row: handle_row(row), axis=1)

        return df.to_dict('records'), department_id_list

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
                pass

        return id_list
