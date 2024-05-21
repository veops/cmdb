# -*- coding:utf-8 -*-

from flask import abort

from api.lib.cmdb.resp_format import ErrFormat
from api.models.cmdb import TopologyView
from api.models.cmdb import TopologyViewGroup
from api.lib.cmdb.ci_type import CITypeRelationManager

class TopologyViewManager(object):
    group_cls = TopologyViewGroup
    cls = TopologyView

    @classmethod
    def upsert_group(cls, name, order):
        if order is None:
            cur_max_order = cls.group_cls.get_by(only_query=True).order_by(cls.group_cls.order.desc()).first()
            cur_max_order = cur_max_order and cur_max_order.order or 0
            order = cur_max_order + 1

        existed = cls.group_cls.get_by(name=name, first=True, to_dict=False)
        if existed is not None:
            return existed.update(order=order)

        return cls.group_cls.create(name=name, order=order)

    @classmethod
    def delete_group(cls, _id):
        existed = cls.group_cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        for item in cls.cls.get_by(group_id=_id, to_dict=False):
            item.update(group_id=None, filter_none=False)

        existed.soft_delete()

    @classmethod
    def group_order(cls, group_ids):
        for idx, group_id in enumerate(group_ids):
            group = cls.group_cls.get_by_id(group_id)
            group.update(order=idx + 1)

    @classmethod
    def add(cls, name, group_id, option, order=None, **kwargs):
        cls.cls.get_by(name=name, first=True) and abort(400, ErrFormat.topology_exists.format(name))
        if order is None:
            cur_max_order = cls.cls.get_by(group_id=group_id, only_query=True).order_by(
                cls.cls.order.desc()).first()
            cur_max_order = cur_max_order and cur_max_order.order or 0
            order = cur_max_order + 1

        return cls.cls.create(name=name, group_id=group_id, option=option, order=order, **kwargs).to_dict()

    @classmethod
    def update(cls, _id, **kwargs):
        existed = cls.cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        return existed.update(filter_none=False, **kwargs).to_dict()

    @classmethod
    def delete(cls, _id):
        existed = cls.cls.get_by_id(_id) or abort(404, ErrFormat.not_found)

        existed.soft_delete()

    @classmethod
    def group_inner_order(cls, _ids):
        for idx, _id in enumerate(_ids):
            topology = cls.cls.get_by_id(_id)
            topology.update(order=idx + 1)

    @classmethod
    def get_all(cls):
        groups = cls.group_cls.get_by(to_dict=True)
        group2pos = {group['id']: idx for idx, group in enumerate(groups)}

        topo_views = cls.cls.get_by(to_dict=True)
        other_group = dict(views=[])
        for view in topo_views:
            if view['group_id']:
                groups[group2pos[view['group_id']]].setdefault('views', []).append(view)
            else:
                other_group['views'].append(view)

        if other_group['views']:
            groups.append(other_group)

        return groups

    @staticmethod
    def relation_from_ci_type(type_id):
        nodes, edges = CITypeRelationManager.get_relations_by_type_id(type_id)

        return dict(nodes=nodes, edges=edges)

    def topology_view(self, view):
        pass
