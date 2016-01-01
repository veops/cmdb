# -*- coding:utf-8 -*- 


from flask import Blueprint
from flask import jsonify
from flask import request

from lib.ci_type import CITypeRelationManager
from lib.auth import auth_with_key


cityperelation = Blueprint("cityperelation", __name__)


@cityperelation.route("/types", methods=["GET"])
def get_types():
    manager = CITypeRelationManager()
    return jsonify(relation_types=manager.relation_types)


@cityperelation.route("/<int:parent>/children", methods=["GET"])
def get_children_by_parent(parent=None):
    manager = CITypeRelationManager()
    return jsonify(children=manager.get_children(parent))


@cityperelation.route("/<int:child>/parents", methods=["GET"])
def get_parents_by_child(child=None):
    manager = CITypeRelationManager()
    return jsonify(parents=manager.get_parents(child))


@cityperelation.route("/<int:parent>/<int:child>", methods=["POST"])
@auth_with_key
def create_citype_realtions(parent=None, child=None):
    relation_type = request.values.get("relation_type", "contain")
    manager = CITypeRelationManager()
    res = manager.add(parent, child, relation_type=relation_type)
    return jsonify(ctr_id=res)


@cityperelation.route("/<int:ctr_id>", methods=["DELETE"])
@auth_with_key
def delete_citype_relation(ctr_id=None):
    manager = CITypeRelationManager()
    manager.delete(ctr_id)
    return jsonify(message="CIType Relation is deleted")


@cityperelation.route("/<int:parent>/<int:child>", methods=["DELETE"])
@auth_with_key
def delete_citype_relation_2(parent=None, child=None):
    manager = CITypeRelationManager()
    manager.delete_2(parent, child)
    return jsonify(message="CIType Relation is deleted")
