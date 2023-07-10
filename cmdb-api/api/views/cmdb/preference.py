# -*- coding:utf-8 -*-


from flask import abort
from flask import request

from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.const import PermEnum, ResourceTypeEnum, RoleEnum
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.preference import PreferenceManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import role_required
from api.lib.perm.acl.acl import validate_permission
from api.lib.utils import handle_arg_list
from api.resource import APIView


class PreferenceShowCITypesView(APIView):
    url_prefix = ("/preference/ci_types", "/preference/ci_types2")

    def get(self):
        instance = request.values.get("instance")
        tree = request.values.get("tree")

        if "ci_types2" in request.url:
            return self.jsonify(PreferenceManager.get_types2(instance, tree))

        return self.jsonify(PreferenceManager.get_types(instance, tree))


class PreferenceShowAttributesView(APIView):
    url_prefix = "/preference/ci_types/<id_or_name>/attributes"

    def get(self, id_or_name):
        is_subscribed, attributes = PreferenceManager.get_show_attributes(id_or_name)

        attr_filter = CIFilterPermsCRUD.get_attr_filter(int(id_or_name)) if str(id_or_name).isdigit() else []

        if attr_filter:
            attributes = [i for i in attributes if i['name'] in attr_filter]

        return self.jsonify(attributes=attributes, is_subscribed=is_subscribed)

    @args_required("attr", value_required=False)
    @args_validate(PreferenceManager.pref_attr_cls)
    def post(self, id_or_name):
        id_or_name = int(id_or_name)
        attr_list = handle_arg_list(request.values.get("attr", ""))  # [[attr, false], ]
        orders = list(range(len(attr_list)))

        if attr_list and not is_app_admin('cmdb'):
            resource_name = CITypeManager.get_name_by_id(id_or_name)
            if not ACLManager('cmdb').has_permission(resource_name, ResourceTypeEnum.CI, PermEnum.READ):
                from api.lib.perm.acl.resp_format import ErrFormat
                return abort(403, ErrFormat.resource_no_permission.format(resource_name, PermEnum.READ))

        PreferenceManager.create_or_update_show_attributes(id_or_name, list(zip(attr_list, orders)))

        return self.jsonify(type_id=id_or_name,
                            attr_order=list(zip(attr_list, orders)))

    @has_perm_from_args("id_or_name", ResourceTypeEnum.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    def put(self, id_or_name):
        return self.post(id_or_name)


class PreferenceTreeApiView(APIView):
    url_prefix = "/preference/tree/view"

    def get(self):
        return self.jsonify(PreferenceManager.get_tree_view())

    @args_required("type_id")
    @args_required("levels", value_required=False)
    @args_validate(PreferenceManager.pref_tree_cls)
    def post(self):
        type_id = request.values.get("type_id")
        levels = handle_arg_list(request.values.get("levels"))
        if levels:
            if not is_app_admin("cmdb"):
                validate_permission(CITypeManager.get_name_by_id(type_id), ResourceTypeEnum.CI, PermEnum.READ)

        res = PreferenceManager.create_or_update_tree_view(type_id, levels)

        return self.jsonify(res and res.to_dict() or {})

    def put(self):
        return self.post()


class PreferenceRelationApiView(APIView):
    url_prefix = "/preference/relation/view"

    def get(self):
        views, id2type, name2id = PreferenceManager.get_relation_view()

        return self.jsonify(views=views, id2type=id2type, name2id=name2id)

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    @args_required("cr_ids")
    @args_validate(PreferenceManager.pref_rel_cls)
    def post(self):
        name = request.values.get("name")
        cr_ids = request.values.get("cr_ids")
        views, id2type, name2id = PreferenceManager.create_or_update_relation_view(name, cr_ids)

        return self.jsonify(views=views, id2type=id2type, name2id=name2id)

    @role_required(RoleEnum.CONFIG)
    def put(self):
        return self.post()

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    def delete(self):
        name = request.values.get("name")
        PreferenceManager.delete_relation_view(name)

        return self.jsonify(name=name)


class PreferenceSearchOptionView(APIView):
    url_prefix = ("/preference/search/option", "/preference/search/option/<int:_id>")

    def get(self):
        res = PreferenceManager.get_search_option(**request.values)

        return self.jsonify(res)

    @args_required("name", value_required=True)
    @args_required("option", value_required=True)
    @args_validate(PreferenceManager.pre_so_cls)
    def post(self):
        res = PreferenceManager.add_search_option(**request.values)

        return self.jsonify(res.to_dict())

    @args_validate(PreferenceManager.pre_so_cls)
    def put(self, _id):
        res = PreferenceManager.update_search_option(_id, **request.values)

        return self.jsonify(res.to_dict())

    def delete(self, _id):
        PreferenceManager.delete_search_option(_id)

        return self.jsonify(id=_id)


class PreferenceRelationGrantView(APIView):
    url_prefix = "/preference/relation/view/roles/<int:rid>/grant"

    def post(self, rid):
        name = request.values.get("name")
        perms = request.values.get('perms')

        acl = ACLManager('cmdb')
        if not acl.has_permission(name, ResourceTypeEnum.RELATION_VIEW, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(name, PermEnum.GRANT))

        acl.grant_resource_to_role_by_rid(name, rid, ResourceTypeEnum.RELATION_VIEW, perms)

        return self.jsonify(code=200)


class PreferenceRelationRevokeView(APIView):
    url_prefix = "/preference/relation/view/roles/<int:rid>/revoke"

    def post(self, rid):
        name = request.values.get("name")
        perms = request.values.get('perms')

        acl = ACLManager('cmdb')
        if not acl.has_permission(name, ResourceTypeEnum.RELATION_VIEW, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(name, PermEnum.GRANT))

        acl.revoke_resource_from_role_by_rid(name, rid, ResourceTypeEnum.RELATION_VIEW, perms)

        return self.jsonify(code=200)
