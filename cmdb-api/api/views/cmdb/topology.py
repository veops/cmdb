# -*- coding:utf-8 -*-

from flask import abort
from flask import request

from api.lib.cmdb.const import PermEnum, ResourceTypeEnum
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.topology import TopologyViewManager
from api.lib.common_setting.decorator import perms_role_required
from api.lib.common_setting.role_perm_base import CMDBApp
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.perm.acl.acl import is_app_admin
from api.resource import APIView

app_cli = CMDBApp()


class TopologyGroupView(APIView):
    url_prefix = ('/topology_views/groups', '/topology_views/groups/<int:group_id>')

    @args_required('name')
    @args_validate(TopologyViewManager.group_cls)
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.create_topology_group, app_cli.admin_name)
    def post(self):
        name = request.values.get('name')
        order = request.values.get('order')

        group = TopologyViewManager.add_group(name, order)

        return self.jsonify(group.to_dict())

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.update_topology_group, app_cli.admin_name)
    def put(self, group_id):
        name = request.values.get('name')
        view_ids = request.values.get('view_ids')
        group = TopologyViewManager().update_group(group_id, name, view_ids)

        return self.jsonify(**group)

    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.delete_topology_group, app_cli.admin_name)
    def delete(self, group_id):
        TopologyViewManager.delete_group(group_id)

        return self.jsonify(group_id=group_id)


class TopologyGroupOrderView(APIView):
    url_prefix = ('/topology_views/groups/order',)

    @args_required('group_ids')
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.update_topology_group, app_cli.admin_name)
    def post(self):
        group_ids = request.values.get('group_ids')

        TopologyViewManager.group_order(group_ids)

        return self.jsonify(group_ids=group_ids)

    def put(self):
        return self.post()


class TopologyView(APIView):
    url_prefix = ('/topology_views', '/topology_views/relations/ci_types/<int:type_id>', '/topology_views/<int:_id>')

    def get(self, type_id=None, _id=None):
        if type_id is not None:
            return self.jsonify(TopologyViewManager.relation_from_ci_type(type_id))

        if _id is not None:
            return self.jsonify(TopologyViewManager().get_view_by_id(_id))

        return self.jsonify(TopologyViewManager.get_all())

    @args_required('name', 'central_node_type', 'central_node_instances', 'path', 'group_id')
    @args_validate(TopologyViewManager.cls)
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.create_topology_view, app_cli.admin_name)
    def post(self):
        name = request.values.pop('name')
        group_id = request.values.pop('group_id', None)
        option = request.values.pop('option', None)
        order = request.values.pop('order', None)

        topo_view = TopologyViewManager.add(name, group_id, option, order, **request.values)

        return self.jsonify(topo_view)

    @args_validate(TopologyViewManager.cls)
    @has_perm_from_args("_id", ResourceTypeEnum.TOPOLOGY_VIEW, PermEnum.UPDATE, TopologyViewManager.get_name_by_id)
    def put(self, _id):
        topo_view = TopologyViewManager.update(_id, **request.values)

        return self.jsonify(topo_view)

    @has_perm_from_args("_id", ResourceTypeEnum.TOPOLOGY_VIEW, PermEnum.DELETE, TopologyViewManager.get_name_by_id)
    def delete(self, _id):
        TopologyViewManager.delete(_id)

        return self.jsonify(code=200)


class TopologyOrderView(APIView):
    url_prefix = ('/topology_views/order',)

    @args_required('view_ids')
    @perms_role_required(app_cli.app_name, app_cli.resource_type_name, app_cli.op.TopologyView,
                         app_cli.op.create_topology_view, app_cli.admin_name)
    def post(self):
        view_ids = request.values.get('view_ids')

        TopologyViewManager.group_inner_order(view_ids)

        return self.jsonify(view_ids=view_ids)

    def put(self):
        return self.post()


class TopologyViewPreview(APIView):
    url_prefix = ('/topology_views/preview', '/topology_views/<int:_id>/view')

    def get(self, _id=None):
        if _id is not None:
            acl = ACLManager('cmdb')
            resource_name = TopologyViewManager.get_name_by_id(_id)
            if (not acl.has_permission(resource_name, ResourceTypeEnum.TOPOLOGY_VIEW, PermEnum.READ) and
                    not is_app_admin('cmdb')):
                return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.READ))

            return self.jsonify(TopologyViewManager().topology_view(view_id=_id))
        else:
            return self.jsonify(TopologyViewManager().topology_view(preview=request.values))

    def post(self, _id=None):
        return self.get(_id)


class TopologyViewGrantView(APIView):
    url_prefix = "/topology_views/<int:view_id>/roles/<int:rid>/grant"

    def post(self, view_id, rid):
        perms = request.values.pop('perms', None)

        view_name = TopologyViewManager.get_name_by_id(view_id) or abort(404, ErrFormat.not_found)
        acl = ACLManager('cmdb')
        if not acl.has_permission(view_name, ResourceTypeEnum.TOPOLOGY_VIEW,
                                  PermEnum.GRANT) and not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(view_name, PermEnum.GRANT))

        acl.grant_resource_to_role_by_rid(view_name, rid, ResourceTypeEnum.TOPOLOGY_VIEW, perms, rebuild=True)

        return self.jsonify(code=200)


class TopologyViewRevokeView(APIView):
    url_prefix = "/topology_views/<int:view_id>/roles/<int:rid>/revoke"

    @args_required('perms')
    def post(self, view_id, rid):
        perms = request.values.pop('perms', None)

        view_name = TopologyViewManager.get_name_by_id(view_id) or abort(404, ErrFormat.not_found)
        acl = ACLManager('cmdb')
        if not acl.has_permission(view_name, ResourceTypeEnum.TOPOLOGY_VIEW,
                                  PermEnum.GRANT) and not is_app_admin('cmdb'):
            return abort(403, ErrFormat.no_permission.format(view_name, PermEnum.GRANT))

        acl.revoke_resource_from_role_by_rid(view_name, rid, ResourceTypeEnum.TOPOLOGY_VIEW, perms, rebuild=True)

        return self.jsonify(code=200)
