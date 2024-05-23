# -*- coding:utf-8 -*-

from flask import request

from api.lib.cmdb.topology import TopologyViewManager
from api.lib.decorator import args_required
from api.lib.decorator import args_validate
from api.resource import APIView


class TopologyGroupView(APIView):
    url_prefix = ('/topology_views/groups', '/topology_views/groups/<int:group_id>')

    @args_required('name')
    @args_validate(TopologyViewManager.group_cls)
    def post(self):
        name = request.values.get('name')
        order = request.values.get('order')

        group = TopologyViewManager.add_group(name, order)

        return self.jsonify(group.to_dict())

    def put(self, group_id):
        name = request.values.get('name')
        view_ids = request.values.get('view_ids')
        group = TopologyViewManager().update_group(group_id, name, view_ids)

        return self.jsonify(**group)

    def delete(self, group_id):
        TopologyViewManager.delete_group(group_id)

        return self.jsonify(group_id=group_id)


class TopologyGroupOrderView(APIView):
    url_prefix = ('/topology_views/groups/order',)

    @args_required('group_ids')
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

    @args_required('name', 'central_node_type', 'central_node_instances', 'path')
    @args_validate(TopologyViewManager.cls)
    def post(self):
        name = request.values.pop('name')
        group_id = request.values.pop('group_id', None)
        option = request.values.pop('option', None)
        order = request.values.pop('order', None)

        topo_view = TopologyViewManager.add(name, group_id, option, order, **request.values)

        return self.jsonify(topo_view)

    @args_validate(TopologyViewManager.cls)
    def put(self, _id):
        topo_view = TopologyViewManager.update(_id, **request.values)

        return self.jsonify(topo_view)

    def delete(self, _id):
        TopologyViewManager.delete(_id)

        return self.jsonify(code=200)


class TopologyOrderView(APIView):
    url_prefix = ('/topology_views/order',)

    @args_required('view_ids')
    def post(self):
        view_ids = request.values.get('view_ids')

        TopologyViewManager.group_inner_order(view_ids)

        return self.jsonify(view_ids=view_ids)

    def put(self):
        return self.post()


class TopologyViewPreview(APIView):
    url_prefix = ('/topology_views/<int:_id>/preview',)

    def get(self, _id):
        return self.jsonify(TopologyViewManager().topology_view(_id))
