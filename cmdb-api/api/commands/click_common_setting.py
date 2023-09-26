import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.datastructures import MultiDict

from api.lib.common_setting.acl import ACLManager
from api.lib.common_setting.employee import EmployeeAddForm
from api.lib.common_setting.resp_format import ErrFormat
from api.models.common_setting import Employee, Department


class InitEmployee(object):
    """
    初始化员工
    """

    def __init__(self):
        self.log = current_app.logger

    def import_user_from_acl(self):
        """
        Import users from ACL
        """

        InitDepartment().init()
        acl = ACLManager('acl')
        user_list = acl.get_all_users()

        username_list = [e['username'] for e in Employee.get_by()]

        for user in user_list:
            acl_uid = user['uid']
            block = 1 if user['block'] else 0
            acl_rid = self.get_rid_by_uid(acl_uid)
            if user['username'] in username_list:
                existed = Employee.get_by(first=True, username=user['username'], to_dict=False)
                if existed:
                    existed.update(
                        acl_uid=acl_uid,
                        acl_rid=acl_rid,
                        block=block,
                    )
                continue
            try:
                form = EmployeeAddForm(MultiDict(user))
                if not form.validate():
                    raise Exception(
                        ','.join(['{}: {}'.format(filed, ','.join(msg)) for filed, msg in form.errors.items()]))
                data = form.data
                data['acl_uid'] = acl_uid
                data['acl_rid'] = acl_rid
                data['block'] = block
                data.pop('password')
                Employee.create(
                    **data
                )
            except Exception as e:
                self.log.error(ErrFormat.acl_import_user_failed.format(user['username'], str(e)))
                self.log.error(e)

    def get_rid_by_uid(self, uid):
        from api.models.acl import Role
        role = Role.get_by(first=True, uid=uid)
        return role['id'] if role is not None else 0


class InitDepartment(object):
    def __init__(self):
        self.log = current_app.logger

    def init(self):
        self.init_wide_company()

    def hard_delete(self, department_id, department_name):
        existed_deleted_list = Department.query.filter(
            Department.department_name == department_name,
            Department.department_id == department_id,
            Department.deleted == 1,
        ).all()
        for existed in existed_deleted_list:
            existed.delete()

    def get_department(self, department_name):
        return Department.query.filter(
            Department.department_name == department_name,
            Department.deleted == 0,
        ).order_by(Department.created_at.asc()).first()

    def run(self, department_id, department_name, department_parent_id):
        self.hard_delete(department_id, department_name)

        res = self.get_department(department_name)
        if res:
            if res.department_id == department_id:
                return
            else:
                new_d = res.update(
                    department_id=department_id,
                    department_parent_id=department_parent_id,
                )
                return

        Department.create(
            department_id=department_id,
            department_name=department_name,
            department_parent_id=department_parent_id,
        )
        new_d = self.get_department(department_name)

        if new_d.department_id != department_id:
            new_d = new_d.update(
                department_id=department_id,
                department_parent_id=department_parent_id,
            )
        self.log.info(f"初始化 {department_name} 部门成功.")

    def run_common(self, department_id, department_name, department_parent_id):
        try:
            self.run(department_id, department_name, department_parent_id)
        except Exception as e:
            current_app.logger.error(f"init {department_name} err:")
            current_app.logger.error(e)
            raise Exception(e)

    def init_wide_company(self):
        """
        创建 id 0, name 全公司 的部门
        """
        department_id = 0
        department_name = '全公司'
        department_parent_id = -1

        self.run_common(department_id, department_name, department_parent_id)

    def create_acl_role_with_department(self):
        """
        当前所有部门，在ACL创建 role
        """
        acl = ACLManager('acl')
        role_name_map = {role['name']: role for role in acl.get_all_roles()}

        d_list = Department.query.filter(
            Department.deleted == 0, Department.department_parent_id != -1).all()
        for department in d_list:
            if department.acl_rid > 0:
                continue

            role = role_name_map.get(department.department_name)
            if role is None:
                payload = {
                    'app_id': 'acl',
                    'name': department.department_name,
                }
                role = acl.create_role(payload)

            acl_rid = role.get('id') if role else 0

            department.update(
                acl_rid=acl_rid
            )
            info = f"update department acl_rid: {acl_rid}"
            current_app.logger.info(info)

    def init_backend_resource(self):
        acl = self.check_app('backend')
        resources_types = acl.get_all_resources_types()

        results = list(filter(lambda t: t['name'] == '操作权限', resources_types['groups']))
        if len(results) == 0:
            payload = dict(
                app_id=acl.app_name,
                name='操作权限',
                description='',
                perms=['read', 'grant', 'delete', 'update']
            )
            resource_type = acl.create_resources_type(payload)
        else:
            resource_type = results[0]

        for name in ['公司信息']:
            payload = dict(
                type_id=resource_type['id'],
                app_id=acl.app_name,
                name=name,
            )
            try:
                acl.create_resource(payload)
            except Exception as e:
                if '已经存在' in str(e):
                    pass
                else:
                    raise Exception(e)

    def check_app(self, app_name):
        acl = ACLManager(app_name)
        payload = dict(
            name=app_name,
            description=app_name
        )
        try:
            app = acl.validate_app()
            if app:
                return acl

            acl.create_app(payload)
        except Exception as e:
            current_app.logger.error(e)
            if '不存在' in str(e):
                acl.create_app(payload)
                return acl
            raise Exception(e)


@click.command()
@with_appcontext
def init_import_user_from_acl():
    """
    Import users from ACL
    """
    InitEmployee().import_user_from_acl()


@click.command()
@with_appcontext
def init_department():
    """
    Department initialization
    """
    cli = InitDepartment()
    cli.init_wide_company()
    cli.create_acl_role_with_department()
    cli.init_backend_resource()


@click.command()
@with_appcontext
def common_check_new_columns():
    """
    add new columns to tables
    """
    from api.extensions import db
    from sqlalchemy import inspect, text

    def get_model_by_table_name(table_name):
        for model in db.Model.registry._class_registry.values():
            if hasattr(model, '__tablename__') and model.__tablename__ == table_name:
                return model
        return None

    def add_new_column(table_name, new_column):
        column_type = new_column.type.compile(engine.dialect)
        default_value = new_column.default.arg if new_column.default else None

        sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column.name} {column_type} "
        if new_column.comment:
            sql += f" comment '{new_column.comment}'"

        if column_type == 'JSON':
            pass
        elif default_value:
            if column_type.startswith('VAR') or column_type.startswith('Text'):
                if default_value is None or len(default_value) == 0:
                    pass
            else:
                sql += f" DEFAULT {default_value}"

        sql = text(sql)
        db.session.execute(sql)

    engine = db.get_engine()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    for table_name in table_names:
        existed_columns = inspector.get_columns(table_name)
        existed_column_name_list = [c['name'] for c in existed_columns]

        model = get_model_by_table_name(table_name)
        if model is None:
            continue
        model_columns = model.__table__.columns._all_columns
        for column in model_columns:
            if column.name not in existed_column_name_list:
                try:
                    add_new_column(table_name, column)
                    current_app.logger.info(f"add new column [{column.name}] in table [{table_name}] success.")
                except Exception as e:
                    current_app.logger.error(f"add new column [{column.name}] in table [{table_name}] err:")
                    current_app.logger.error(e)
