# -*- coding:utf-8 -*-

from flask import request
from flask_login import current_user

from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl import validate_app
from api.lib.perm.acl.resource import ResourceCRUD
from api.lib.perm.acl.resource import ResourceGroupCRUD
from api.lib.perm.acl.resource import ResourceTypeCRUD
from api.lib.perm.auth import auth_only_for_acl
from api.lib.perm.auth import auth_with_app_token
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.resource import APIView


class ResourceTypeView(APIView):
    url_prefix = ("/resource_types", "/resource_types/<int:type_id>")

    @validate_app
    @auth_with_app_token
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')

        numfound, res, id2perms = ResourceTypeCRUD.search(q, app_id, page, page_size)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            groups=[i.to_dict() for i in res],
                            id2perms=id2perms)

    @args_required('name')
    @args_required('perms')
    @validate_app
    @auth_only_for_acl
    @args_validate(ResourceTypeCRUD.cls, exclude_args=['app_id'])
    def post(self):
        name = request.values.get('name')
        app_id = request.values.get('app_id')
        description = request.values.get('description', '')
        perms = request.values.get('perms')

        rt = ResourceTypeCRUD.add(app_id, name, description, perms)

        return self.jsonify(rt.to_dict())

    @auth_only_for_acl
    @args_validate(ResourceTypeCRUD.cls, exclude_args=['app_id'])
    def put(self, type_id):
        rt = ResourceTypeCRUD.update(type_id, **request.values)

        return self.jsonify(rt.to_dict())

    @auth_only_for_acl
    def delete(self, type_id):
        ResourceTypeCRUD.delete(type_id)

        return self.jsonify(type_id=type_id)


class ResourceTypePermsView(APIView):
    url_prefix = "/resource_types/<int:type_id>/perms"

    @auth_with_app_token
    def get(self, type_id):
        return self.jsonify(ResourceTypeCRUD.get_perms(type_id))


class ResourceView(APIView):
    url_prefix = ("/resources", "/resources/<int:resource_id>")

    @validate_app
    @auth_with_app_token
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        u = request.values.get('u')
        resource_type_id = request.values.get('resource_type_id')
        app_id = request.values.get('app_id')

        numfound, res = ResourceCRUD.search(q, u, app_id, resource_type_id, page, page_size)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            resources=res)

    @args_required('name')
    @args_required('type_id')
    @validate_app
    @auth_only_for_acl
    @args_validate(ResourceCRUD.cls, exclude_args=['app_id'])
    def post(self):
        name = request.values.get('name')
        type_id = request.values.get('type_id')
        app_id = request.values.get('app_id')
        uid = request.values.get('uid')
        if not uid and hasattr(current_user, "uid"):
            uid = current_user.uid

        resource = ResourceCRUD.add(name, type_id, app_id, uid)

        return self.jsonify(resource.to_dict())

    @args_required('name')
    @auth_only_for_acl
    @args_validate(ResourceCRUD.cls, exclude_args=['app_id'])
    def put(self, resource_id):
        name = request.values.get('name')

        resource = ResourceCRUD.update(resource_id, name)

        return self.jsonify(resource.to_dict())

    @auth_only_for_acl
    def delete(self, resource_id):
        ResourceCRUD.delete(resource_id)

        return self.jsonify(resource_id=resource_id)


class ResourceGroupView(APIView):
    url_prefix = ("/resource_groups", "/resource_groups/<int:group_id>")

    @validate_app
    @auth_with_app_token
    def get(self):
        page = get_page(request.values.get("page", 1))
        page_size = get_page_size(request.values.get("page_size"))
        q = request.values.get('q')
        app_id = request.values.get('app_id')
        resource_type_id = request.values.get('resource_type_id')

        numfound, res = ResourceGroupCRUD.search(q, app_id, resource_type_id, page, page_size)

        return self.jsonify(numfound=numfound,
                            page=page,
                            page_size=page_size,
                            groups=[i.to_dict() for i in res])

    @args_required('name')
    @args_required('type_id')
    @validate_app
    @auth_only_for_acl
    @args_validate(ResourceGroupCRUD.cls, exclude_args=['app_id'])
    def post(self):
        name = request.values.get('name')
        type_id = request.values.get('type_id')
        app_id = request.values.get('app_id')

        group = ResourceGroupCRUD.add(name, type_id, app_id)

        return self.jsonify(group.to_dict())

    @args_required('items')
    @auth_only_for_acl
    @args_validate(ResourceGroupCRUD.cls, exclude_args=['app_id'])
    def put(self, group_id):
        items = handle_arg_list(request.values.get("items"))

        ResourceGroupCRUD.update(group_id, items)

        items = ResourceGroupCRUD.get_items(group_id)

        return self.jsonify(items)

    @auth_only_for_acl
    def delete(self, group_id):
        ResourceGroupCRUD.delete(group_id)

        return self.jsonify(group_id=group_id)


class ResourceGroupItemsView(APIView):
    url_prefix = "/resource_groups/<int:group_id>/items"

    @auth_with_app_token
    def get(self, group_id):
        items = ResourceGroupCRUD.get_items(group_id)

        return self.jsonify(items)
