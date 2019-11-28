# -*- coding:utf-8 -*-

import json

import six
import toposort
from flask import abort
from flask import g

from api.extensions import db
from api.lib.cmdb.attribute import AttributeManager
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import PreferenceRelationView
from api.models.cmdb import PreferenceShowAttributes
from api.models.cmdb import PreferenceTreeView


class PreferenceManager(object):
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
    def get_show_attributes(type_id):
        if not isinstance(type_id, six.integer_types):
            type_id = CITypeCache.get(type_id).id

        attrs = db.session.query(PreferenceShowAttributes, CITypeAttribute.order).join(
            CITypeAttribute, CITypeAttribute.attr_id == PreferenceShowAttributes.attr_id).filter(
            PreferenceShowAttributes.uid == g.user.uid).filter(
            PreferenceShowAttributes.type_id == type_id).filter(
            PreferenceShowAttributes.deleted.is_(False)).filter(CITypeAttribute.deleted.is_(False)).filter(
            CITypeAttribute.type_id == type_id).order_by(
            CITypeAttribute.order).all()
        result = [i.PreferenceShowAttributes.attr.to_dict() for i in attrs]
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
                i.update(dict(choice_value=AttributeManager.get_choice_values(i["id"], i["value_type"])))

        return is_subscribed, result

    @classmethod
    def create_or_update_show_attributes(cls, type_id, attr_order):
        existed_all = PreferenceShowAttributes.get_by(type_id=type_id, uid=g.user.uid, to_dict=False)
        for _attr, order in attr_order:
            attr = AttributeCache.get(_attr) or abort(404, "Attribute <{0}> does not exist".format(_attr))
            existed = PreferenceShowAttributes.get_by(type_id=type_id,
                                                      uid=g.user.uid,
                                                      attr_id=attr.id,
                                                      first=True,
                                                      to_dict=False)
            if existed is None:
                PreferenceShowAttributes.create(type_id=type_id,
                                                uid=g.user.uid,
                                                attr_id=attr.id,
                                                order=order)
            else:
                existed.update(order=order)

        attr_dict = {int(i): j for i, j in attr_order}
        for i in existed_all:
            if i.attr_id not in attr_dict:
                i.soft_delete()

    @staticmethod
    def get_tree_view():
        res = PreferenceTreeView.get_by(uid=g.user.uid, to_dict=True)
        for item in res:
            if item["levels"]:
                item.update(CITypeCache.get(item['type_id']).to_dict())
                item.update(dict(levels=[AttributeCache.get(l).to_dict()
                                         for l in item["levels"].split(",") if AttributeCache.get(l)]))

        return res

    @staticmethod
    def create_or_update_tree_view(type_id, levels):
        attrs = CITypeAttributeCache.get(type_id)
        for idx, i in enumerate(levels):
            for attr in attrs:
                attr = AttributeCache.get(attr.attr_id)
                if i == attr.id or i == attr.name or i == attr.alias:
                    levels[idx] = str(attr.id)
        levels = ",".join(levels)

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
        views = PreferenceRelationView.get_by(to_dict=True)
        result = dict()
        name2id = list()
        for view in views:
            result.setdefault(view['name'], []).extend(json.loads(view['cr_ids']))
            name2id.append([view['name'], view['id']])

        id2type = dict()
        for view_name in result:
            for i in result[view_name]:
                id2type[i['parent_id']] = None
                id2type[i['child_id']] = None

            result[view_name] = toposort.toposort_flatten(
                {i['child_id']: {i['parent_id']} for i in result[view_name]})

        for type_id in id2type:
            id2type[type_id] = CITypeCache.get(type_id).to_dict()

        return result, id2type, sorted(name2id, key=lambda x: x[1])

    @classmethod
    def create_or_update_relation_view(cls, name, cr_ids):
        existed = PreferenceRelationView.get_by(name=name, to_dict=False, first=True)
        if existed is None:
            return PreferenceRelationView.create(name=name, cr_ids=json.dumps(cr_ids))

        return cls.get_relation_view()

    @staticmethod
    def delete_relation_view(name):
        for existed in PreferenceRelationView.get_by(name=name, to_dict=False):
            existed.soft_delete()
        return name
