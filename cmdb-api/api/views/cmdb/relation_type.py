# -*- coding:utf-8 -*-


from flask import abort
from flask import request

from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.relation_type import RelationTypeManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import role_required
from api.resource import APIView


class RelationTypeView(APIView):
    url_prefix = ("/relation_types", "/relation_types/<int:rel_id>")

    def get(self):
        return self.jsonify([i.to_dict() for i in RelationTypeManager.get_all()])

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    @args_validate(RelationTypeManager.cls)
    def post(self):
        name = request.values.get("name") or abort(400, ErrFormat.argument_value_required.format("name"))
        rel = RelationTypeManager.add(name)

        return self.jsonify(rel.to_dict())

    @role_required(RoleEnum.CONFIG)
    @args_required("name")
    @args_validate(RelationTypeManager.cls)
    def put(self, rel_id):
        name = request.values.get("name") or abort(400, ErrFormat.argument_value_required.format("name"))
        rel = RelationTypeManager.update(rel_id, name)

        return self.jsonify(rel.to_dict())

    @role_required(RoleEnum.CONFIG)
    def delete(self, rel_id):
        RelationTypeManager.delete(rel_id)

        return self.jsonify(rel_id=rel_id)
