# -*- coding:utf-8 -*- 


from flask import abort
from flask import request

from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.decorator import args_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import role_required
from api.resource import APIView


class GetChildrenView(APIView):
    url_prefix = ("/ci_type_relations/<int:parent_id>/children",
                  "/ci_type_relations/<int:parent_id>/recursive_level2children",
                  )

    def get(self, parent_id):
        if request.url.endswith("recursive_level2children"):
            return self.jsonify(CITypeRelationManager.recursive_level2children(parent_id))

        return self.jsonify(children=CITypeRelationManager.get_children(parent_id))


class GetParentsView(APIView):
    url_prefix = "/ci_type_relations/<int:child_id>/parents"

    def get(self, child_id):
        return self.jsonify(parents=CITypeRelationManager.get_parents(child_id))


class CITypeRelationView(APIView):
    url_prefix = ("/ci_type_relations", "/ci_type_relations/<int:parent_id>/<int:child_id>")

    @role_required(RoleEnum.CONFIG)
    def get(self):
        res = CITypeRelationManager.get()

        return self.jsonify(res)

    @has_perm_from_args("parent_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    @args_required("relation_type_id")
    def post(self, parent_id, child_id):
        relation_type_id = request.values.get("relation_type_id")
        constraint = request.values.get("constraint")
        ctr_id = CITypeRelationManager.add(parent_id, child_id, relation_type_id, constraint)

        return self.jsonify(ctr_id=ctr_id)

    @has_perm_from_args("parent_id", ResourceTypeEnum.CI, PermEnum.CONFIG, CITypeManager.get_name_by_id)
    def delete(self, parent_id, child_id):
        CITypeRelationManager.delete_2(parent_id, child_id)

        return self.jsonify(code=200, parent_id=parent_id, child_id=child_id)


class CITypeRelationDelete2View(APIView):
    url_prefix = "/ci_type_relations/<int:ctr_id>"

    @role_required(RoleEnum.CONFIG)
    def delete(self, ctr_id):
        CITypeRelationManager.delete(ctr_id)

        return self.jsonify(code=200, ctr_id=ctr_id)


class CITypeRelationGrantView(APIView):
    url_prefix = "/ci_type_relations/<int:parent_id>/<int:child_id>/roles/<int:rid>/grant"

    def post(self, parent_id, child_id, rid):
        p = CITypeManager.check_is_existed(parent_id)
        c = CITypeManager.check_is_existed(child_id)
        resource_name = CITypeRelationManager.acl_resource_name(p.name, c.name)

        perms = request.values.get('perms')

        acl = ACLManager('cmdb')
        if not acl.has_permission(resource_name, ResourceTypeEnum.CI_TYPE_RELATION, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.GRANT))

        acl.grant_resource_to_role_by_rid(resource_name, rid, ResourceTypeEnum.CI_TYPE_RELATION, perms)

        return self.jsonify(code=200)


class CITypeRelationRevokeView(APIView):
    url_prefix = "/ci_type_relations/<int:parent_id>/<int:child_id>/roles/<int:rid>/revoke"

    def post(self, parent_id, child_id, rid):
        p = CITypeManager.check_is_existed(parent_id)
        c = CITypeManager.check_is_existed(child_id)
        resource_name = CITypeRelationManager.acl_resource_name(p.name, c.name)

        perms = request.values.get('perms')
        acl = ACLManager('cmdb')
        if not acl.has_permission(resource_name, ResourceTypeEnum.CI_TYPE_RELATION, PermEnum.GRANT) and \
                not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.GRANT))

        acl.revoke_resource_from_role_by_rid(resource_name, rid, ResourceTypeEnum.CI_TYPE_RELATION, perms)

        return self.jsonify(code=200)
