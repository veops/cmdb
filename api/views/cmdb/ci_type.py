# -*- coding:utf-8 -*- 


from flask import abort
from flask import current_app
from flask import request

from api.resource import APIView
from api.lib.perm.acl import role_required
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.ci_type import CITypeGroupManager
from api.lib.cmdb.ci_type import CITypeAttributeGroupManager
from api.lib.decorator import args_required
from api.lib.utils import handle_arg_list


class CITypeView(APIView):
    url_prefix = ("/ci_types", "/ci_types/<int:type_id>", "/ci_types/<string:type_name>")

    def get(self, type_id=None, type_name=None):
        q = request.args.get("type_name")

        if type_id is not None:
            ci_types = [CITypeCache.get(type_id).to_dict()]
        elif type_name is not None:
            ci_types = [CITypeCache.get(type_name).to_dict()]
        else:
            ci_types = CITypeManager().get_ci_types(q)
        count = len(ci_types)

        return self.jsonify(numfound=count, ci_types=ci_types)

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    def post(self):
        params = request.values

        type_name = params.get("name")
        type_alias = params.get("alias")
        type_alias = type_name if not type_alias else type_alias
        params['alias'] = type_alias

        manager = CITypeManager()
        type_id = manager.add(**params)

        return self.jsonify(type_id=type_id)

    @role_required(RoleEnum.CONFIG)
    def put(self, type_id):
        params = request.values

        manager = CITypeManager()
        manager.update(type_id, **params)
        return self.jsonify(type_id=type_id)

    @role_required(RoleEnum.CONFIG)
    def delete(self, type_id):
        CITypeManager.delete(type_id)
        return self.jsonify(type_id=type_id)


class CITypeGroupView(APIView):
    url_prefix = ("/ci_types/groups", "/ci_types/groups/<int:gid>")

    def get(self):
        need_other = request.values.get("need_other")
        return self.jsonify(CITypeGroupManager.get(need_other))

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    def post(self):
        name = request.values.get("name")
        group = CITypeGroupManager.add(name)
        return self.jsonify(group.to_dict())

    @role_required(RoleEnum.CONFIG)
    def put(self, gid):
        name = request.values.get('name')
        type_ids = request.values.get('type_ids')
        CITypeGroupManager.update(gid, name, type_ids)
        return self.jsonify(gid=gid)

    @role_required(RoleEnum.CONFIG)
    def delete(self, gid):
        CITypeGroupManager.delete(gid)
        return self.jsonify(gid=gid)


class CITypeQueryView(APIView):
    url_prefix = "/ci_types/query"

    @args_required("q")
    def get(self):
        q = request.args.get("q")
        res = CITypeManager.query(q)
        return self.jsonify(ci_type=res)


class EnableCITypeView(APIView):
    url_prefix = "/ci_types/<int:type_id>/enable"

    @role_required(RoleEnum.CONFIG)
    def post(self, type_id):
        enable = request.values.get("enable", True)
        CITypeManager.set_enabled(type_id, enabled=enable)
        return self.jsonify(type_id=type_id, enable=enable)


class CITypeAttributeView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/attributes", "/ci_types/<string:type_name>/attributes")

    def get(self, type_id=None, type_name=None):
        t = CITypeCache.get(type_id) or CITypeCache.get(type_name) or abort(404, "CIType does not exist")
        type_id = t.id
        unique_id = t.unique_id
        unique = AttributeCache.get(unique_id).name
        return self.jsonify(attributes=CITypeAttributeManager.get_attributes_by_type_id(type_id),
                            type_id=type_id,
                            unique_id=unique_id,
                            unique=unique)

    @role_required(RoleEnum.CONFIG)
    @args_required("attr_id")
    def post(self, type_id=None):
        attr_id_list = handle_arg_list(request.values.get("attr_id"))
        params = request.values
        params.pop("attr_id",  "")

        CITypeAttributeManager.add(type_id, attr_id_list, **params)
        return self.jsonify(attributes=attr_id_list)

    @role_required(RoleEnum.CONFIG)
    @args_required("attributes")
    def put(self, type_id=None):
        """
        attributes is list, only support raw data request
        :param type_id: 
        :return: 
        """
        attributes = request.values.get("attributes")
        current_app.logger.debug(attributes)
        if not isinstance(attributes, list):
            return abort(400, "attributes must be list")
        CITypeAttributeManager.update(type_id, attributes)
        return self.jsonify(attributes=attributes)

    @role_required(RoleEnum.CONFIG)
    @args_required("attr_id")
    def delete(self, type_id=None):
        """
        Form request: attr_id is a string, separated by commas
        Raw data request: attr_id is a list
        :param type_id: 
        :return: 
        """
        attr_id_list = handle_arg_list(request.values.get("attr_id", ""))

        CITypeAttributeManager.delete(type_id, attr_id_list)

        return self.jsonify(attributes=attr_id_list)


class CITypeAttributeGroupView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/attribute_groups",
                  "/ci_types/attribute_groups/<int:group_id>")

    def get(self, type_id):
        need_other = request.values.get("need_other")
        return self.jsonify(CITypeAttributeGroupManager.get_by_type_id(type_id, need_other))

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    def post(self, type_id):
        name = request.values.get("name").strip()
        order = request.values.get("order") or 0
        attrs = handle_arg_list(request.values.get("attributes", ""))
        orders = list(range(len(attrs)))

        attr_order = list(zip(attrs, orders))
        group = CITypeAttributeGroupManager.create_or_update(type_id, name, attr_order, order)
        current_app.logger.warning(group.id)
        return self.jsonify(group_id=group.id)

    @role_required(RoleEnum.CONFIG)
    def put(self, group_id):
        name = request.values.get("name")
        order = request.values.get("order") or 0
        attrs = handle_arg_list(request.values.get("attributes", ""))
        orders = list(range(len(attrs)))

        attr_order = list(zip(attrs, orders))
        CITypeAttributeGroupManager.update(group_id, name, attr_order, order)
        return self.jsonify(group_id=group_id)

    @role_required(RoleEnum.CONFIG)
    def delete(self, group_id):
        CITypeAttributeGroupManager.delete(group_id)
        return self.jsonify(group_id=group_id)
