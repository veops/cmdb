# -*- coding:utf-8 -*-

from flask import request

from api.lib.decorator import args_required
from api.lib.perm.acl.role import RoleCRUD
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.resource import APIView


class RoleView(APIView):
    url_prefix = ("/roles", "/roles/<int:rid>")

    @args_required('app_id')
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')

        numfound, roles = RoleCRUD.search(q, app_id, page, page_size)

        id2parents = RoleRelationCRUD.get_parents([i.id for i in roles])

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            id2parents=id2parents,
                            roles=[i.to_dict() for i in roles])

    @args_required('name')
    @args_required('app_id')
    def post(self):
        name = request.values.get('name')
        app_id = request.values.get('app_id')
        is_app_admin = request.values.get('is_app_admin', False)

        role = RoleCRUD.add_role(name, app_id, is_app_admin=is_app_admin)

        return self.jsonify(role.to_dict())

    def put(self, rid):
        role = RoleCRUD.update_role(rid, **request.values)

        return self.jsonify(role.to_dict())

    def delete(self, rid):
        RoleCRUD.delete_role(rid)

        return self.jsonify(rid=rid)


class RoleRelationView(APIView):
    url_prefix = "/roles/<int:child_id>/parents"

    @args_required('parent_id')
    def post(self, child_id):
        parent_id = request.values.get('parent_id')
        res = RoleRelationCRUD.add(parent_id, child_id)

        return self.jsonify(res.to_dict())

    @args_required('parent_id')
    def delete(self, child_id):
        parent_id = request.values.get('parent_id')

        RoleRelationCRUD.delete2(parent_id, child_id)

        return self.jsonify(parent_id=parent_id, child_id=child_id)
