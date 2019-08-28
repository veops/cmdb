# -*- coding:utf-8 -*- 


from flask import request

from api.lib.perm.acl import role_required
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.decorator import args_required
from api.resource import APIView


class GetChildrenView(APIView):
    url_prefix = "/ci_type_relations/<int:parent_id>/children"

    def get(self, parent_id):
        return self.jsonify(children=CITypeRelationManager.get_children(parent_id))


class GetParentsView(APIView):
    url_prefix = "/ci_type_relations/<int:child_id>/parents"

    def get(self, child_id):
        return self.jsonify(parents=CITypeRelationManager.get_parents(child_id))


class CITypeRelationView(APIView):
    url_prefix = "/ci_type_relations/<int:parent_id>/<int:child_id>"

    @role_required(RoleEnum.CONFIG)
    @args_required("relation_type_id")
    def post(self, parent_id, child_id):
        relation_type_id = request.values.get("relation_type_id")
        ctr_id = CITypeRelationManager.add(parent_id, child_id, relation_type_id)
        return self.jsonify(ctr_id=ctr_id)

    @role_required(RoleEnum.CONFIG)
    def delete(self, parent_id, child_id):
        CITypeRelationManager.delete_2(parent_id, child_id)
        return self.jsonify(code=200, parent_id=parent_id, child_id=child_id)


class CITypeRelationDelete2View(APIView):
    url_prefix = "/ci_type_relations/<int:ctr_id>"

    @role_required(RoleEnum.CONFIG)
    def delete(self, ctr_id):
        CITypeRelationManager.delete(ctr_id)
        return self.jsonify(code=200, ctr_id=ctr_id)
