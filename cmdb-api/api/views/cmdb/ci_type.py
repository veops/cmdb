# -*- coding:utf-8 -*-


import json
from io import BytesIO

from flask import abort
from flask import current_app
from flask import request
from flask import session

from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci_type import CITypeAttributeGroupManager
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci_type import CITypeGroupManager
from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.ci_type import CITypeTemplateManager
from api.lib.cmdb.ci_type import CITypeTriggerManager
from api.lib.cmdb.ci_type import CITypeUniqueConstraintManager
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
from api.lib.perm.acl.cache import AppCache
from api.lib.perm.acl.role import RoleCRUD
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.auth import auth_with_app_token
from api.lib.utils import handle_arg_list
from api.resource import APIView


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

    @args_required("name")
    @args_validate(CITypeManager.cls)
    def post(self):
        params = request.values

        type_name = params.get("name")
        type_alias = params.get("alias")
        type_alias = type_name if not type_alias else type_alias
        params['alias'] = type_alias

        manager = CITypeManager()
        type_id = manager.add(**params)

        return self.jsonify(type_id=type_id)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_validate(CITypeManager.cls)
    def put(self, type_id):
        params = request.values

        manager = CITypeManager()
        manager.update(type_id, **params)

        return self.jsonify(type_id=type_id)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def delete(self, type_id):
        CITypeManager.delete(type_id)

        return self.jsonify(type_id=type_id)


class CITypeGroupView(APIView):
    url_prefix = ("/ci_types/groups",
                  "/ci_types/groups/config",
                  "/ci_types/groups/order",
                  "/ci_types/groups/<int:gid>")

    def get(self):
        config_required = True if "/config" in request.url else False
        need_other = request.values.get("need_other")

        return self.jsonify(CITypeGroupManager.get(need_other, config_required))

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    @args_validate(CITypeGroupManager.cls)
    def post(self):
        name = request.values.get("name")
        group = CITypeGroupManager.add(name)

        return self.jsonify(group.to_dict())

    @args_validate(CITypeGroupManager.cls)
    def put(self, gid=None):
        if "/order" in request.url:
            if RoleEnum.CONFIG not in session.get("acl", {}).get("parentRoles", []) and not is_app_admin("cmdb"):
                return abort(403, ErrFormat.role_required.format(RoleEnum.CONFIG))

            group_ids = request.values.get('group_ids')
            CITypeGroupManager.order(group_ids)

            return self.jsonify(group_ids=group_ids)

        name = request.values.get('name') or abort(400, ErrFormat.argument_value_required.format("name"))
        type_ids = request.values.get('type_ids')

        CITypeGroupManager.update(gid, name, type_ids)

        return self.jsonify(gid=gid)

    @role_required(RoleEnum.CONFIG)
    def delete(self, gid):
        type_ids = request.values.get("type_ids")
        CITypeGroupManager.delete(gid, type_ids)

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

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def post(self, type_id):
        enable = request.values.get("enable", True)
        CITypeManager.set_enabled(type_id, enabled=enable)

        return self.jsonify(type_id=type_id, enable=enable)


class CITypeAttributeView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/attributes", "/ci_types/<string:type_name>/attributes",
                  "/ci_types/common_attributes")

    def get(self, type_id=None, type_name=None):
        if request.path.endswith("/common_attributes"):
            type_ids = handle_arg_list(request.values.get('type_ids'))

            return self.jsonify(attributes=CITypeAttributeManager.get_common_attributes(type_ids))

        t = CITypeCache.get(type_id) or CITypeCache.get(type_name) or abort(404, ErrFormat.ci_type_not_found)
        type_id = t.id
        unique_id = t.unique_id
        unique = AttributeCache.get(unique_id).name

        attr_filter = CIFilterPermsCRUD.get_attr_filter(type_id)
        attributes = CITypeAttributeManager.get_attributes_by_type_id(type_id)
        if attr_filter:
            attributes = [i for i in attributes if i['name'] in attr_filter]

        return self.jsonify(attributes=attributes,
                            type_id=type_id,
                            unique_id=unique_id,
                            unique=unique)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("attr_id")
    def post(self, type_id=None):
        attr_id_list = handle_arg_list(request.values.get("attr_id"))
        params = request.values
        params.pop("attr_id", "")

        CITypeAttributeManager.add(type_id, attr_id_list, **params)

        return self.jsonify(attributes=attr_id_list)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
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
            return abort(400, ErrFormat.argument_attributes_must_be_list)

        CITypeAttributeManager.update(type_id, attributes)

        return self.jsonify(attributes=attributes)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
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


class CITypesAttributeView(APIView):
    url_prefix = ("/ci_types/attributes",)

    @args_required("type_ids", value_required=True)
    def get(self):
        type_ids = handle_arg_list(request.values.get('type_ids'))

        attr_names = set()
        attributes = list()
        for type_id in type_ids:
            _attributes = CITypeAttributeManager.get_attributes_by_type_id(type_id)
            for _attr in _attributes:
                if _attr['name'] not in attr_names:
                    attr_names.add(_attr['name'])
                    attributes.append(_attr)

        return self.jsonify(attributes=attributes)


class CITypeAttributeTransferView(APIView):
    url_prefix = "/ci_types/<int:type_id>/attributes/transfer"

    @args_required('from')
    @args_required('to')
    def post(self, type_id):
        _from = request.values.get('from')  # {'attr_id': xx, 'group_id': xx}
        _to = request.values.get('to')  # {'group_id': xx, 'order': xxx}

        CITypeAttributeManager.transfer(type_id, _from, _to)

        return self.jsonify(code=200)


class CITypeAttributeGroupTransferView(APIView):
    url_prefix = "/ci_types/<int:type_id>/attribute_groups/transfer"

    @args_required('from')
    @args_required('to')
    def post(self, type_id):
        _from = request.values.get('from')  # group_id
        _to = request.values.get('to')  # group_id

        CITypeAttributeGroupManager.transfer(type_id, _from, _to)

        return self.jsonify(code=200)


class CITypeAttributeGroupView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/attribute_groups",
                  "/ci_types/attribute_groups/<int:group_id>")

    def get(self, type_id):
        need_other = request.values.get("need_other")
        groups = CITypeAttributeGroupManager.get_by_type_id(type_id, need_other)

        attr_filter = CIFilterPermsCRUD.get_attr_filter(type_id)
        if attr_filter:
            for group in groups:
                group['attributes'] = [attr for attr in (group.get('attributes') or []) if attr['name'] in attr_filter]

        return self.jsonify(groups)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("name")
    @args_validate(CITypeAttributeGroupManager.cls)
    def post(self, type_id):
        name = request.values.get("name").strip()
        order = request.values.get("order") or 0
        attrs = handle_arg_list(request.values.get("attributes", ""))
        orders = list(range(len(attrs)))

        attr_order = list(zip(attrs, orders))
        group = CITypeAttributeGroupManager.create_or_update(type_id, name, attr_order, order)
        current_app.logger.warning(group.id)
        return self.jsonify(group_id=group.id)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("name")
    @args_validate(CITypeAttributeGroupManager.cls)
    def put(self, group_id):
        name = request.values.get("name")
        order = request.values.get("order") or 0
        attrs = handle_arg_list(request.values.get("attributes", ""))
        orders = list(range(len(attrs)))

        attr_order = list(zip(attrs, orders))
        CITypeAttributeGroupManager.update(group_id, name, attr_order, order)
        return self.jsonify(group_id=group_id)

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def delete(self, group_id):
        CITypeAttributeGroupManager.delete(group_id)
        return self.jsonify(group_id=group_id)


class CITypeTemplateView(APIView):
    url_prefix = ("/ci_types/template/import", "/ci_types/template/export")

    @role_required(RoleEnum.CONFIG)
    def get(self):  # export
        return self.jsonify(
            dict(ci_type_template=CITypeTemplateManager.export_template()))

    @role_required(RoleEnum.CONFIG)
    def post(self):  # import
        tpt = request.values.get('ci_type_template') or {}

        CITypeTemplateManager().import_template(tpt)

        return self.jsonify(code=200)


class CITypeCanDefineComputed(APIView):
    url_prefix = "/ci_types/can_define_computed"

    @role_required(PermEnum.CONFIG)
    def get(self):
        return self.jsonify(code=200)


class CITypeTemplateFileView(APIView):
    url_prefix = ("/ci_types/template/import/file", "/ci_types/template/export/file")

    @role_required(RoleEnum.CONFIG)
    def get(self):  # export
        tpt_json = CITypeTemplateManager.export_template()
        tpt_json = dict(ci_type_template=tpt_json)

        bf = BytesIO()
        bf.write(bytes(json.dumps(tpt_json).encode('utf-8')))
        bf.seek(0)

        return self.send_file(bf,
                              as_attachment=True,
                              download_name="cmdb_template.json",
                              mimetype='application/json',
                              max_age=0)

    @role_required(RoleEnum.CONFIG)
    def post(self):  # import
        f = request.files.get('file')

        if f is None:
            return abort(400, ErrFormat.argument_file_not_found)

        content = f.read()
        try:
            content = json.loads(content)
        except:
            return abort(400, ErrFormat.invalid_json)
        tpt = content.get('ci_type_template')

        CITypeTemplateManager().import_template(tpt)

        return self.jsonify(code=200)


class CITypeUniqueConstraintView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/unique_constraint", "/ci_types/<int:type_id>/unique_constraint/<int:_id>")

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def get(self, type_id):
        return self.jsonify(CITypeUniqueConstraintManager.get_detail(type_id))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("attr_ids")
    def post(self, type_id):
        attr_ids = request.values.get('attr_ids')

        return self.jsonify(CITypeUniqueConstraintManager().add(type_id, attr_ids))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("attr_ids")
    def put(self, type_id, _id):
        assert type_id is not None

        attr_ids = request.values.get('attr_ids')

        return self.jsonify(CITypeUniqueConstraintManager().update(_id, attr_ids))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def delete(self, type_id, _id):
        assert type_id is not None

        CITypeUniqueConstraintManager().delete(_id)

        return self.jsonify(code=200)


class CITypeTriggerView(APIView):
    url_prefix = ("/ci_types/<int:type_id>/triggers", "/ci_types/<int:type_id>/triggers/<int:_id>")

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def get(self, type_id):
        return self.jsonify(CITypeTriggerManager.get(type_id))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("option")
    def post(self, type_id):
        attr_id = request.values.get('attr_id') or None
        option = request.values.get('option')

        return self.jsonify(CITypeTriggerManager().add(type_id, attr_id, option))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("option")
    def put(self, type_id, _id):
        assert type_id is not None

        option = request.values.get('option')
        attr_id = request.values.get('attr_id')

        return self.jsonify(CITypeTriggerManager().update(_id, attr_id, option))

    @has_perm_from_args("type_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def delete(self, type_id, _id):
        assert type_id is not None

        CITypeTriggerManager().delete(_id)

        return self.jsonify(code=200)


class CITypeGrantView(APIView):
    url_prefix = "/ci_types/<int:type_id>/roles/<int:rid>/grant"

    def post(self, type_id, rid):
        perms = request.values.pop('perms', None)

        if request.values.get('attr_filter'):
            request.values['attr_filter'] = handle_arg_list(request.values.get('attr_filter', ''))

        _type = CITypeCache.get(type_id)
        type_name = _type and _type.name or abort(404, ErrFormat.ci_type_not_found)
        acl = ACLManager('cmdb')
        if not acl.has_permission(type_name, ResourceTypeEnum.CI_TYPE, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(type_name, PermEnum.GRANT))

        acl.grant_resource_to_role_by_rid(type_name, rid, ResourceTypeEnum.CI_TYPE, perms)

        CIFilterPermsCRUD().add(type_id=type_id, rid=rid, **request.values)

        return self.jsonify(code=200)


class CITypeRevokeView(APIView):
    url_prefix = "/ci_types/<int:type_id>/roles/<int:rid>/revoke"

    @args_required('perms')
    def post(self, type_id, rid):
        perms = request.values.pop('perms', None)

        if request.values.get('attr_filter'):
            request.values['attr_filter'] = handle_arg_list(request.values.get('attr_filter', ''))

        _type = CITypeCache.get(type_id)
        type_name = _type and _type.name or abort(404, ErrFormat.ci_type_not_found)
        acl = ACLManager('cmdb')
        if not acl.has_permission(type_name, ResourceTypeEnum.CI_TYPE, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(type_name, PermEnum.GRANT))

        acl.revoke_resource_from_role_by_rid(type_name, rid, ResourceTypeEnum.CI_TYPE, perms)

        if PermEnum.READ in perms:
            CIFilterPermsCRUD().delete(type_id=type_id, rid=rid)

            app_id = AppCache.get('cmdb').id
            users = RoleRelationCRUD.get_users_by_rid(rid, app_id)
            for i in (users or []):
                if i.get('role', {}).get('id') and not RoleCRUD.has_permission(
                        i.get('role').get('id'), type_name, ResourceTypeEnum.CI_TYPE, app_id, PermEnum.READ):
                    PreferenceManager.delete_by_type_id(type_id, i.get('uid'))

        return self.jsonify(type_id=type_id, rid=rid)


class CITypeFilterPermissionView(APIView):
    url_prefix = "/ci_types/<int:type_id>/filters/permissions"

    @auth_with_app_token
    def get(self, type_id):
        return self.jsonify(CIFilterPermsCRUD().get(type_id))
