# -*- coding:utf-8 -*-


import copy

import six
import toposort
from flask import abort
from flask import current_app
from flask_login import current_user

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.cache import CMDBCounterCache
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import PermEnum
from api.lib.cmdb.const import ResourceTypeEnum
from api.lib.cmdb.const import RoleEnum
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.exception import AbortException
from api.lib.perm.acl.acl import ACLManager
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeRelation
from api.models.cmdb import PreferenceCITypeOrder
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
        ci_type_order = sorted(PreferenceCITypeOrder.get_by(uid=current_user.uid, to_dict=False), key=lambda x: x.order)

        types = db.session.query(PreferenceShowAttributes.type_id).filter(
            PreferenceShowAttributes.uid == current_user.uid).filter(
            PreferenceShowAttributes.deleted.is_(False)).group_by(
            PreferenceShowAttributes.type_id).all() if instance else []
        types = sorted(types, key=lambda x: {i.type_id: idx for idx, i in enumerate(
            ci_type_order) if not i.is_tree}.get(x.type_id, 1))

        tree_types = PreferenceTreeView.get_by(uid=current_user.uid, to_dict=False) if tree else []
        tree_types = sorted(tree_types, key=lambda x: {i.type_id: idx for idx, i in enumerate(
            ci_type_order) if i.is_tree}.get(x.type_id, 1))

        type_ids = [i.type_id for i in types + tree_types]
        if types and tree_types:
            type_ids = set(type_ids)

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
        result = dict(self=dict(instance=[], tree=[], type_id2subs_time=dict()))

        result.update(CMDBCounterCache.get_sub_counter())

        ci_type_order = sorted(PreferenceCITypeOrder.get_by(uid=current_user.uid, to_dict=False), key=lambda x: x.order)
        if instance:
            types = db.session.query(PreferenceShowAttributes.type_id,
                                     PreferenceShowAttributes.uid, PreferenceShowAttributes.created_at).filter(
                PreferenceShowAttributes.deleted.is_(False)).filter(
                PreferenceShowAttributes.uid == current_user.uid).group_by(
                PreferenceShowAttributes.uid, PreferenceShowAttributes.type_id)
            for i in types:
                result['self']['instance'].append(i.type_id)
                if str(i.created_at) > str(result['self']['type_id2subs_time'].get(i.type_id, "")):
                    result['self']['type_id2subs_time'][i.type_id] = i.created_at

            instance_order = [i.type_id for i in ci_type_order if not i.is_tree]
            if len(instance_order) == len(result['self']['instance']):
                result['self']['instance'] = instance_order

        if tree:
            types = PreferenceTreeView.get_by(uid=current_user.uid, to_dict=False)
            for i in types:
                result['self']['tree'].append(i.type_id)
                if str(i.created_at) > str(result['self']['type_id2subs_time'].get(i.type_id, "")):
                    result['self']['type_id2subs_time'][i.type_id] = i.created_at

            tree_order = [i.type_id for i in ci_type_order if i.is_tree]
            if len(tree_order) == len(result['self']['tree']):
                result['self']['tree'] = tree_order

        return result

    @staticmethod
    def get_show_attributes(type_id):
        if not isinstance(type_id, six.integer_types):
            _type = CITypeCache.get(type_id)
            type_id = _type and _type.id

        attrs = db.session.query(PreferenceShowAttributes, CITypeAttribute.order).join(
            CITypeAttribute, CITypeAttribute.attr_id == PreferenceShowAttributes.attr_id).filter(
            PreferenceShowAttributes.uid == current_user.uid).filter(
            PreferenceShowAttributes.type_id == type_id).filter(
            PreferenceShowAttributes.deleted.is_(False)).filter(CITypeAttribute.deleted.is_(False)).group_by(
            CITypeAttribute.attr_id).all()

        result = []
        for i in sorted(attrs, key=lambda x: x.PreferenceShowAttributes.order):
            item = i.PreferenceShowAttributes.attr.to_dict()
            item.update(dict(is_fixed=i.PreferenceShowAttributes.is_fixed))
            result.append(item)

        is_subscribed = True
        if not attrs:
            result = CITypeAttributeManager.get_attributes_by_type_id(type_id,
                                                                      choice_web_hook_parse=False,
                                                                      choice_other_parse=False)
            result = [i for i in result if i['default_show']]
            is_subscribed = False

        for i in result:
            if i["is_choice"]:
                i.update(dict(choice_value=AttributeManager.get_choice_values(
                    i["id"], i["value_type"], i.get("choice_web_hook"), i.get("choice_other"))))

        return is_subscribed, result

    @classmethod
    def create_or_update_show_attributes(cls, type_id, attr_order):
        existed_all = PreferenceShowAttributes.get_by(type_id=type_id, uid=current_user.uid, to_dict=False)
        for x, order in attr_order:
            if isinstance(x, list):
                _attr, is_fixed = x
            else:
                _attr, is_fixed = x, False
            attr = AttributeCache.get(_attr) or abort(404, ErrFormat.attribute_not_found.format("id={}".format(_attr)))
            existed = PreferenceShowAttributes.get_by(type_id=type_id,
                                                      uid=current_user.uid,
                                                      attr_id=attr.id,
                                                      first=True,
                                                      to_dict=False)
            if existed is None:
                PreferenceShowAttributes.create(type_id=type_id,
                                                uid=current_user.uid,
                                                attr_id=attr.id,
                                                order=order,
                                                is_fixed=is_fixed)
            else:
                existed.update(order=order, is_fixed=is_fixed)

        attr_dict = {int(i[0]) if isinstance(i, list) else int(i): j for i, j in attr_order}
        for i in existed_all:
            if i.attr_id not in attr_dict:
                i.soft_delete()

        if not existed_all and attr_order:
            cls.add_ci_type_order_item(type_id, is_tree=False)

        elif not PreferenceShowAttributes.get_by(type_id=type_id, uid=current_user.uid, to_dict=False):
            cls.delete_ci_type_order_item(type_id, is_tree=False)

    @staticmethod
    def get_tree_view():
        ci_type_order = sorted(PreferenceCITypeOrder.get_by(uid=current_user.uid, is_tree=True, to_dict=False),
                               key=lambda x: x.order)

        res = PreferenceTreeView.get_by(uid=current_user.uid, to_dict=True)
        if ci_type_order:
            res = sorted(res, key=lambda x: {ii.type_id: idx for idx, ii in enumerate(
                ci_type_order)}.get(x['type_id'], 1))

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

    @classmethod
    def create_or_update_tree_view(cls, type_id, levels):
        attrs = CITypeAttributesCache.get(type_id)
        for idx, i in enumerate(levels):
            for attr in attrs:
                attr = AttributeCache.get(attr.attr_id)
                if i == attr.id or i == attr.name or i == attr.alias:
                    levels[idx] = attr.id

        existed = PreferenceTreeView.get_by(uid=current_user.uid, type_id=type_id, to_dict=False, first=True)
        if existed is not None:
            if not levels:
                existed.soft_delete()
                cls.delete_ci_type_order_item(type_id, is_tree=True)
                return existed
            return existed.update(levels=levels)
        elif levels:
            cls.add_ci_type_order_item(type_id, is_tree=True)

            return PreferenceTreeView.create(levels=levels, type_id=type_id, uid=current_user.uid)

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
        name2view = dict()
        result = dict()
        name2id = list()
        for view in views:
            view2cr_ids.setdefault(view['name'], []).extend(view['cr_ids'])
            name2id.append([view['name'], view['id']])
            name2view[view['name']] = view

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

            for _l in leaf:
                _find_parent(_l)

            for node_id in node2show_types:
                node2show_types[node_id] = [CITypeCache.get(i).to_dict() for i in set(node2show_types[node_id])]

            topo_flatten = list(toposort.toposort_flatten(topo))
            level2constraint = {}
            for i, _ in enumerate(topo_flatten[1:]):
                ctr = CITypeRelation.get_by(
                    parent_id=topo_flatten[i], child_id=topo_flatten[i + 1], first=True, to_dict=False)
                level2constraint[i + 1] = ctr and ctr.constraint

            if leaf2show_types.get(topo_flatten[-1]):
                ctr = CITypeRelation.get_by(
                    parent_id=topo_flatten[-1],
                    child_id=leaf2show_types[topo_flatten[-1]][0], first=True, to_dict=False)
                level2constraint[len(topo_flatten)] = ctr and ctr.constraint

            result[view_name] = dict(topo=list(map(list, toposort.toposort(topo))),
                                     topo_flatten=topo_flatten,
                                     level2constraint=level2constraint,
                                     leaf=leaf,
                                     option=name2view[view_name]['option'],
                                     is_public=name2view[view_name]['is_public'],
                                     leaf2show_types=leaf2show_types,
                                     node2show_types=node2show_types,
                                     show_types=[CITypeCache.get(j).to_dict()
                                                 for i in leaf2show_types.values() for j in i])

        for type_id in id2type:
            id2type[type_id] = CITypeCache.get(type_id).to_dict()

        return result, id2type, sorted(name2id, key=lambda x: x[1])

    @classmethod
    def create_or_update_relation_view(cls, name=None, cr_ids=None, _id=None, is_public=False, option=None):
        if not cr_ids:
            return abort(400, ErrFormat.preference_relation_view_node_required)

        if _id is None:
            existed = PreferenceRelationView.get_by(name=name, to_dict=False, first=True)
        else:
            existed = PreferenceRelationView.get_by_id(_id)
        current_app.logger.debug(existed)
        if existed is None:
            PreferenceRelationView.create(name=name, cr_ids=cr_ids, uid=current_user.uid,
                                          is_public=is_public, option=option)

            if current_app.config.get("USE_ACL"):
                ACLManager().add_resource(name, ResourceTypeEnum.RELATION_VIEW)
                ACLManager().grant_resource_to_role(name,
                                                    RoleEnum.CMDB_READ_ALL,
                                                    ResourceTypeEnum.RELATION_VIEW,
                                                    permissions=[PermEnum.READ])
        else:
            if existed.name != name and current_app.config.get("USE_ACL"):
                ACLManager().update_resource(existed.name, name, ResourceTypeEnum.RELATION_VIEW)

            existed.update(name=name, cr_ids=cr_ids, is_public=is_public, option=option)

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
        query = query.filter(PreferenceSearchOption.uid == current_user.uid)

        for k in kwargs:
            if hasattr(PreferenceSearchOption, k) and kwargs[k]:
                query = query.filter(getattr(PreferenceSearchOption, k) == kwargs[k])

        return [i.to_dict() for i in query]

    @staticmethod
    def add_search_option(**kwargs):
        kwargs['uid'] = current_user.uid

        existed = PreferenceSearchOption.get_by(uid=current_user.uid,
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

        if current_user.uid != existed.uid:
            return abort(400, ErrFormat.no_permission2)

        other = PreferenceSearchOption.get_by(uid=current_user.uid,
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

        if current_user.uid != existed.uid:
            return abort(400, ErrFormat.no_permission2)

        existed.soft_delete()

    @staticmethod
    def delete_by_type_id(type_id, uid):
        for i in PreferenceShowAttributes.get_by(type_id=type_id, uid=uid, to_dict=False):
            i.soft_delete()

        for i in PreferenceTreeView.get_by(type_id=type_id, uid=uid, to_dict=False):
            i.soft_delete()

        for i in PreferenceCITypeOrder.get_by(type_id=type_id, uid=uid, to_dict=False):
            i.soft_delete()

    @staticmethod
    def can_edit_relation(parent_id, child_id):
        views = PreferenceRelationView.get_by(to_dict=False)
        for view in views:
            has_m2m = False
            last_node_id = None
            for cr in view.cr_ids:
                _rel = CITypeRelation.get_by(parent_id=cr['parent_id'], child_id=cr['child_id'],
                                             first=True, to_dict=False)
                if _rel and _rel.constraint == ConstraintEnum.Many2Many:
                    has_m2m = True

                    if parent_id == _rel.parent_id and child_id == _rel.child_id:
                        return False

                if _rel:
                    last_node_id = _rel.child_id

            if parent_id == last_node_id:
                rels = CITypeRelation.get_by(parent_id=last_node_id, to_dict=False)
                for rel in rels:
                    if rel.child_id == child_id and has_m2m:
                        return False

        return True

    @staticmethod
    def add_ci_type_order_item(type_id, is_tree=False):
        max_order = PreferenceCITypeOrder.get_by(
            uid=current_user.uid, is_tree=is_tree, only_query=True).order_by(PreferenceCITypeOrder.order.desc()).first()
        order = (max_order and max_order.order + 1) or 1

        PreferenceCITypeOrder.create(type_id=type_id, is_tree=is_tree, uid=current_user.uid, order=order)

    @staticmethod
    def delete_ci_type_order_item(type_id, is_tree=False):
        existed = PreferenceCITypeOrder.get_by(uid=current_user.uid, type_id=type_id, is_tree=is_tree,
                                               first=True, to_dict=False)

        existed and existed.soft_delete()

    @staticmethod
    def upsert_ci_type_order(type_ids, is_tree=False):
        for idx, type_id in enumerate(type_ids):
            order = idx + 1
            existed = PreferenceCITypeOrder.get_by(uid=current_user.uid, type_id=type_id, is_tree=is_tree,
                                                   to_dict=False, first=True)
            if existed is not None:
                existed.update(order=order, flush=True)
            else:
                PreferenceCITypeOrder.create(uid=current_user.uid, type_id=type_id, is_tree=is_tree, order=order,
                                             flush=True)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("upsert citype order failed: {}".format(e))
            return abort(400, ErrFormat.unknown_error)
