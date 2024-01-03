# -*- coding:utf-8 -*-
from flask import abort
from flask import request
from werkzeug.datastructures import MultiDict

from api.lib.common_setting.department import DepartmentCRUD
from api.lib.common_setting.department import DepartmentTree, DepartmentForm
from api.lib.common_setting.employee import EmployeeCRUD
from api.lib.common_setting.resp_format import ErrFormat
from api.resource import APIView

prefix = '/department'


class DepartmentAllView(APIView):
    url_prefix = (f'{prefix}/all',)

    def get(self):
        is_tree = int(request.args.get('is_tree', 1))

        res = DepartmentTree().get_all_departments(is_tree)
        return self.jsonify(res)


class DepartmentAllViewWithEmployee(APIView):
    url_prefix = (f'{prefix}/all_with_employee',)

    def get(self):
        block = int(request.args.get('block', -1))
        try:
            res = DepartmentCRUD.get_all_departments_with_employee(block)
            return self.jsonify(res)
        except Exception as e:
            abort(500, str(e))


class DepartmentView(APIView):
    url_prefix = (f'{prefix}',)

    def get(self):
        department_parent_id = request.args.get('department_parent_id', 0)
        block = int(request.args.get('block', 0))

        departments, department_id_list = DepartmentCRUD.get_departments_and_ids(
            department_parent_id, block)
        employees = EmployeeCRUD.get_employees_by_department_id(
            department_parent_id, block)

        return self.jsonify(departments=departments, employees=employees)

    def post(self):
        form = DepartmentForm(MultiDict(request.json))
        if not form.validate():
            abort(400, ','.join(['{}: {}'.format(filed, ','.join(msg))
                                 for filed, msg in form.errors.items()]))

        data = DepartmentCRUD.add(**form.data)

        return self.jsonify(data.to_dict())


class DepartmentIDView(APIView):
    url_prefix = (f'{prefix}/<int:_id>',)

    def put(self, _id):
        form = DepartmentForm(MultiDict(request.json))
        if not form.validate():
            abort(400, ','.join(['{}: {}'.format(filed, ','.join(msg))
                                 for filed, msg in form.errors.items()]))

        department_parent_id = form.data.get('department_parent_id')
        if int(_id) == int(department_parent_id):
            abort(400, ErrFormat.parent_department_is_not_self)

        data = DepartmentCRUD.edit(_id, **form.data)
        return self.jsonify(data.to_dict())

    def delete(self, _id):
        if _id in [-1, 0]:
            abort(400, ErrFormat.delete_reserved_department_name)
        DepartmentCRUD.delete(_id)
        return self.jsonify(status='success')


class DepartmentParentView(APIView):
    url_prefix = (f'{prefix}/allow_parent',)

    def get(self):
        department_id = request.args.get('department_id', None)
        if department_id is None:
            abort(400, ErrFormat.department_id_is_required)

        p_department_list = DepartmentCRUD.get_allow_parent_d_id_by(
            int(department_id))
        return self.jsonify(p_department_list)


class DepartmentSortView(APIView):
    url_prefix = (f'{prefix}/update_sort',)

    def put(self):
        """
        only can sort in the same parent
        """
        department_list = request.json.get('department_list', None)
        if department_list is None:
            abort(400, ErrFormat.department_list_is_required)

        result = DepartmentCRUD.update_department_sort(department_list)

        return self.jsonify(result)
