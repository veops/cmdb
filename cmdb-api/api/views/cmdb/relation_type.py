# -*- coding:utf-8 -*-


from flask import abort
from flask import request

from api.lib.cmdb.relation_type import RelationTypeManager
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.resource import APIView

app_cli = CMDBApp()


class RelationTypeView(APIView):
    url_prefix = ("/relation_types", "/relation_types/<int:rel_id>")

    def get(self):
        return self.jsonify([i.to_dict() for i in RelationTypeManager.get_all()])

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Relationship_Types,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("name")
    @args_validate(RelationTypeManager.cls)
    def post(self):
        name = request.values.get("name") or abort(400, ErrFormat.argument_value_required.format("name"))
        rel = RelationTypeManager.add(name)

        return self.jsonify(rel.to_dict())

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Relationship_Types,
                         app_cli.op.read, app_cli.admin_name)
    @args_required("name")
    @args_validate(RelationTypeManager.cls)
    def put(self, rel_id):
        name = request.values.get("name") or abort(400, ErrFormat.argument_value_required.format("name"))
        rel = RelationTypeManager.update(rel_id, name)

        return self.jsonify(rel.to_dict())

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.Relationship_Types,
                         app_cli.op.read, app_cli.admin_name)
    def delete(self, rel_id):
        RelationTypeManager.delete(rel_id)

        return self.jsonify(rel_id=rel_id)
