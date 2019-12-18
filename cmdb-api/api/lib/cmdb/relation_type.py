# -*- coding:utf-8 -*-


from flask import abort

from api.models.cmdb import RelationType


class RelationTypeManager(object):
    @staticmethod
    def get_all():
        return RelationType.get_by(to_dict=False)

    @classmethod
    def get_names(cls):
        return [i.name for i in cls.get_all()]

    @classmethod
    def get_pairs(cls):
        return [(i.id, i.name) for i in cls.get_all()]

    @staticmethod
    def add(name):
        RelationType.get_by(name=name, first=True, to_dict=False) and abort(400, "It's already existed")
        return RelationType.create(name=name)

    @staticmethod
    def update(rel_id, name):
        existed = RelationType.get_by_id(rel_id) or abort(404, "RelationType <{0}> does not exist".format(rel_id))

        return existed.update(name=name)

    @staticmethod
    def delete(rel_id):
        existed = RelationType.get_by_id(rel_id) or abort(404, "RelationType <{0}> does not exist".format(rel_id))

        existed.soft_delete()
