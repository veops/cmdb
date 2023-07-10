# -*- coding:utf-8 -*-


import copy

import six
import toposort
from flask import abort
from flask import current_app
from flask import g

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.const import PermEnum, ResourceTypeEnum, RoleEnum
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.exception import AbortException
from api.lib.perm.acl.acl import ACLManager
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeRelation
from api.models.cmdb import PreferenceRelationView
from api.models.cmdb import PreferenceSearchOption
from api.models.cmdb import PreferenceShowAttributes
from api.models.cmdb import PreferenceTreeView


class PreferenceManager(object):
    pref_attr_cls = PreferenceShowAttributes
    pref_tree_cls = PreferenceTreeView
    pref_rel_cls = PreferenceRelationView
    pre_so_cls = PreferenceSearchOption

    @staticmethod
    def get_types(instance=False, tree=False):
        types = db.session.query(PreferenceShowAttributes.type_id).filter(
            PreferenceShowAttributes.uid == g.user.uid).filter(
            PreferenceShowAttributes.deleted.is_(False)).group_by(PreferenceShowAttributes.type_id).all() \
            if instance else []
        tree_types = PreferenceTreeView.get_by(uid=g.user.uid, to_dict=False) if tree else []
        type_ids = list(set([i.type_id for i in types + tree_types]))
        return [CITypeCache.get(type_id).to_dict() for type_id in type_ids]

    @staticmethod
    def get_types2(instance=False, tree=False):
        """
        {
            self: {instance: [], tree: [], type_id2subs_time: {type_id: subs_time}},
            type_id2users: {type_id: []}
        }
        :param instance:
        :param tree:
        :return:
        """
        result = dict(self=dict(instance=[], tree=[], type_id2subs_time=dict()),
                      type_id2users=dict())
        if instance:
            types = db.session.query(PreferenceShowAttributes.type_id,
                                     PreferenceShowAttributes.uid, PreferenceShowAttributes.created_at).filter(
                PreferenceShowAttributes.deleted.is_(False)).group_by(
                PreferenceShowAttributes.uid, PreferenceShowAttributes.type_id)
            for i in types:
                if i.uid == g.user.uid:
                    result['self']['instance'].append(i.type_id)
                    if str(i.created_at) > str(result['self']['type_id2subs_time'].get(i.type_id, "")):
                        result['self']['type_id2subs_time'][i.type_id] = i.created_at

                result['type_id2users'].setdefault(i.type_id, []).append(i.uid)

        if tree:
            types = PreferenceTreeView.get_by(to_dict=False)
            for i in types:
                if i.uid == g.user.uid:
                    result['self']['tree'].append(i.type_id)
                    if str(i.created_at) > str(result['self']['type_id2subs_time'].get(i.type_id, "")):
                        result['self']['type_id2subs_time'][i.type_id] = i.created_at

                result['type_id2users'].setdefault(i.type_id, [])
                if i.uid not in result['type_id2users'][i.type_id]:
                    result['type_id2users'][i.type_id].append(i.uid)

        return result

    @staticmethod
    def get_show_attributes(type_id):
        if not isinstance(type_id, six.integer_types):
            _type = CITypeCache.get(type_id)
            type_id = _type and _type.id

        attrs = db.session.query(PreferenceShowAttributes, CITypeAttribute.order).join(
            CITypeAttribute, CITypeAttribute.attr_id == PreferenceShowAttributes.attr_id).filter(
            PreferenceShowAttributes.uid == g.user.uid).filter(
            PreferenceShowAttributes.type_id == type_id).filter(
            PreferenceShowAttributes.deleted.is_(False)).filter(CITypeAttribute.deleted.is_(False)).filter(
            CITypeAttribute.type_id == type_id).all()

        result = []
        for i in sorted(attrs, key=lambda x: x.PreferenceShowAttributes.order):
            item = i.PreferenceShowAttributes.attr.to_dict()
            item.update(dict(is_fixed=i.PreferenceShowAttributes.is_fixed))
            result.append(item)

        is_subscribed = True
        if not attrs:
            attrs = db.session.query(CITypeAttribute).filter(
                CITypeAttribute.type_id == type_id).filter(
                CITypeAttribute.deleted.is_(False)).filter(
                CITypeAttribute.default_show.is_(True)).order_by(CITypeAttribute.order)
            result = [i.attr.to_dict() for i in attrs]
            is_subscribed = False

        for i in result:
            if i["is_choice"]:
                i.update(dict(choice_value=AttributeManager.get_choice_values(
                    i["id"], i["value_type"], i["choice_web_hook"])))

        return is_subscribed, result

    @classmethod
    def create_or_update_show_attributes(cls, type_id, attr_order):
        existed_all = PreferenceShowAttributes.get_by(type_id=type_id, uid=g.user.uid, to_dict=False)
        for x, order in attr_order:
            if isinstance(x, list):
                _attr, is_fixed = x
            else:
                _attr, is_fixed = x, False
            attr = AttributeCache.get(_attr) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_attr)))
            existed = PreferenceShowAttributes.get_by(type_id=type_id,
                                                      uid=g.user.uid,
                                                      attr_id=attr.id,
                                                      first=True,
                                                      to_dict=False)
            if existed is None:
                PreferenceShowAttributes.create(type_id=type_id,
                                                uid=g.user.uid,
                                                attr_id=attr.id,
                                                order=order,
                                                is_fixed=is_fixed)
            else:
                existed.update(order=order, is_fixed=is_fixed)

        attr_dict = {int(i[0]) if isinstance(i, list) else int(i): j for i, j in attr_order}
        for i in existed_all:
            if i.attr_id not in attr_dict:
                i.soft_delete()

    @staticmethod
    def get_tree_view():
        res = PreferenceTreeView.get_by(uid=g.user.uid, to_dict=True)
        for item in res:
            if item["levels"]:
                ci_type = CITypeCache.get(item['type_id']).to_dict()
                attr_filter = CIFilterPermsCRUD.get_attr_filter(ci_type['id'])
                ci_type.pop('id', None)
                ci_type.pop('created_at', None)
                ci_type.pop('updated_at', None)
                item.update(ci_type)

                _levels = []
                for i in item["levels"]:
                    attr = AttributeCache.get(i)
                    if attr and (not attr_filter or attr.name in attr_filter):
                        _levels.append(attr.to_dict())
                item.update(dict(levels=_levels))

        return res

    @staticmethod
    def create_or_update_tree_view(type_id, levels):
        attrs = CITypeAttributesCache.get(type_id)
        for idx, i in enumerate(levels):
            for attr in attrs:
                attr = AttributeCache.get(attr.attr_id)
                if i == attr.id or i == attr.name or i == attr.alias:
                    levels[idx] = attr.id

        existed = PreferenceTreeView.get_by(uid=g.user.uid, type_id=type_id, to_dict=False, first=True)
        if existed is not None:
            if not levels:
                existed.soft_delete()
                return existed
            return existed.update(levels=levels)
        elif levels:
            return PreferenceTreeView.create(levels=levels, type_id=type_id, uid=g.user.uid)

    @staticmethod
    def get_relation_view():
        _views = PreferenceRelationView.get_by(to_dict=True)
        views = []
        if current_app.config.get("USE_ACL"):
            for i in _views:
                try:
                    if i.get('is_public') or ACLManager().has_permission(i.get('name'),
                                                                         ResourceTypeEnum.RELATION_VIEW,
                                                                         PermEnum.READ):
                        views.append(i)
                except AbortException:
                    pass
        else:
            views = _views

        view2cr_ids = dict()
        result = dict()
        name2id = list()
        for view in views:
            view2cr_ids.setdefault(view['name'], []).extend(view['cr_ids'])
            name2id.append([view['name'], view['id']])

        id2type = dict()
        for view_name in view2cr_ids:
            for i in view2cr_ids[view_name]:
                id2type[i['parent_id']] = None
                id2type[i['child_id']] = None
            topo = {i['child_id']: {i['parent_id']} for i in view2cr_ids[view_name]}
            leaf = list(set(toposort.toposort_flatten(topo)) - set([j for i in topo.values() for j in i]))

            leaf2show_types = {i: [t['child_id'] for t in CITypeRelation.get_by(parent_id=i)] for i in leaf}
            node2show_types = copy.deepcopy(leaf2show_types)

            def _find_parent(_node_id):
                parents = topo.get(_node_id, {})
                for parent in parents:
                    node2show_types.setdefault(parent, []).extend(node2show_types.get(_node_id, []))
                    _find_parent(parent)
                if not parents:
                    return

            for l in leaf:
                _find_parent(l)

            for node_id in node2show_types:
                node2show_types[node_id] = [CITypeCache.get(i).to_dict() for i in set(node2show_types[node_id])]

            result[view_name] = dict(topo=list(map(list, toposort.toposort(topo))),
                                     topo_flatten=list(toposort.toposort_flatten(topo)),
                                     leaf=leaf,
                                     leaf2show_types=leaf2show_types,
                                     node2show_types=node2show_types,
                                     show_types=[CITypeCache.get(j).to_dict()
                                                 for i in leaf2show_types.values() for j in i])

        for type_id in id2type:
            id2type[type_id] = CITypeCache.get(type_id).to_dict()

        return result, id2type, sorted(name2id, key=lambda x: x[1])

    @classmethod
    def create_or_update_relation_view(cls, name, cr_ids, is_public=False):
        if not cr_ids:
            return abort(400, ErrFormat.preference_relation_view_node_required)

        existed = PreferenceRelationView.get_by(name=name, to_dict=False, first=True)
        current_app.logger.debug(existed)
        if existed is None:
            PreferenceRelationView.create(name=name, cr_ids=cr_ids, uid=g.user.uid, is_public=is_public)

            if current_app.config.get("USE_ACL"):
                ACLManager().add_resource(name, ResourceTypeEnum.RELATION_VIEW)
                ACLManager().grant_resource_to_role(name,
                                                    RoleEnum.CMDB_READ_ALL,
                                                    ResourceTypeEnum.RELATION_VIEW,
                                                    permissions=[PermEnum.READ])

        return cls.get_relation_view()

    @staticmethod
    def delete_relation_view(name):
        for existed in PreferenceRelationView.get_by(name=name, to_dict=False):
            existed.soft_delete()

        if current_app.config.get("USE_ACL"):
            ACLManager().del_resource(name, ResourceTypeEnum.RELATION_VIEW)

        return name

    @staticmethod
    def get_search_option(**kwargs):
        query = PreferenceSearchOption.get_by(only_query=True)
        query = query.filter(PreferenceSearchOption.uid == g.user.uid)

        for k in kwargs:
            if hasattr(PreferenceSearchOption, k) and kwargs[k]:
                query = query.filter(getattr(PreferenceSearchOption, k) == kwargs[k])

        return [i.to_dict() for i in query]

    @staticmethod
    def add_search_option(**kwargs):
        kwargs['uid'] = g.user.uid

        existed = PreferenceSearchOption.get_by(uid=g.user.uid,
                                                name=kwargs.get('name'),
                                                prv_id=kwargs.get('prv_id'),
                                                ptv_id=kwargs.get('ptv_id'),
                                                type_id=kwargs.get('type_id'),
                                                )
        if existed:
            return abort(400, ErrFormat.preference_search_option_exists)

        return PreferenceSearchOption.create(**kwargs)

    @staticmethod
    def update_search_option(_id, **kwargs):

        existed = PreferenceSearchOption.get_by_id(_id) or abort(404, ErrFormat.preference_search_option_not_found)

        if g.user.uid != existed.uid:
            return abort(400, ErrFormat.no_permission2)

        other = PreferenceSearchOption.get_by(uid=g.user.uid,
                                              name=kwargs.get('name'),
                                              prv_id=kwargs.get('prv_id'),
                                              ptv_id=kwargs.get('ptv_id'),
                                              type_id=kwargs.get('type_id'),
                                              )
        if other.id != _id:
            return abort(400, ErrFormat.preference_search_option_exists)

        return existed.update(**kwargs)

    @staticmethod
    def delete_search_option(_id):
        existed = PreferenceSearchOption.get_by_id(_id) or abort(404, ErrFormat.preference_search_option_not_found)

        if g.user.uid != existed.uid:
            return abort(400, ErrFormat.no_permission2)

        existed.soft_delete()

    @staticmethod
    def delete_by_type_id(type_id, uid):
        for i in PreferenceShowAttributes.get_by(type_id=type_id, uid=uid, to_dict=False):
            i.soft_delete()

        for i in PreferenceTreeView.get_by(type_id=type_id, uid=uid, to_dict=False):
            i.soft_delete()
