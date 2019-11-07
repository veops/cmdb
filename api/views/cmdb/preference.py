# -*- coding:utf-8 -*-


from flask import request

from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.const import ResourceType, PermEnum
from api.lib.cmdb.preference import PreferenceManager
from api.lib.decorator import args_required
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.utils import handle_arg_list
from api.resource import APIView


class PreferenceShowCITypesView(APIView):
    url_prefix = "/preference/ci_types"

    def get(self):
        instance = request.values.get("instance")
        tree = request.values.get("tree")
        return self.jsonify(PreferenceManager.get_types(instance, tree))


class PreferenceShowAttributesView(APIView):
    url_prefix = "/preference/ci_types/<id_or_name>/attributes"

    def get(self, id_or_name):
        is_subscribed, attributes = PreferenceManager.get_show_attributes(id_or_name)
        return self.jsonify(attributes=attributes, is_subscribed=is_subscribed)

    @has_perm_from_args("id_or_name", ResourceType.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    @args_required("attr")
    def post(self, id_or_name):
        id_or_name = int(id_or_name)
        attr_list = handle_arg_list(request.values.get("attr", ""))
        orders = list(range(len(attr_list)))
        PreferenceManager.create_or_update_show_attributes(id_or_name, list(zip(attr_list, orders)))
        return self.jsonify(type_id=id_or_name,
                            attr_order=list(zip(attr_list, orders)))

    @has_perm_from_args("id_or_name", ResourceType.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    def put(self, id_or_name):
        self.post(id_or_name)


class PreferenceTreeApiView(APIView):
    url_prefix = "/preference/tree/view"

    def get(self):
        return self.jsonify(PreferenceManager.get_tree_view())

    @has_perm_from_args("type_id", ResourceType.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    @args_required("type_id")
    @args_required("levels")
    def post(self):
        type_id = request.values.get("type_id")
        levels = handle_arg_list(request.values.get("levels"))
        res = PreferenceManager.create_or_update_tree_view(type_id, levels)
        return self.jsonify(res and res.to_dict() or {})

    def put(self):
        self.post()


class PreferenceRelationApiView(APIView):
    url_prefix = "/preference/relation/view"

    def get(self):
        return self.jsonify(PreferenceManager.get_relation_view())

    @has_perm_from_args("parent_id", ResourceType.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    @has_perm_from_args("child_id", ResourceType.CI, PermEnum.READ, CITypeManager.get_name_by_id)
    @args_required("name")
    def post(self):
        name = request.values.get("name")
        parent_id = request.values.get("parent_id")
        child_id = request.values.get("child_id")
        res = PreferenceManager.create_or_update_relation_view(name, parent_id, child_id)
        return self.jsonify(res.to_dict())

    def put(self):
        self.post()

    @args_required("name")
    def delete(self):
        name = request.values.get("name")
        PreferenceManager.delete_relation_view(name)
        return self.jsonify(name=name)
