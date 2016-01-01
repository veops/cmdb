# -*- coding:utf-8 -*- 


from flask import Blueprint
from flask import jsonify
from flask import request

from lib.ci import CIRelationManager
from lib.utils import get_page
from lib.utils import get_per_page
from lib.auth import auth_with_key


cirelation = Blueprint("cirelation", __name__)


@cirelation.route("/types", methods=["GET"])
def get_types():
    manager = CIRelationManager()
    return jsonify(relation_types=manager.relation_types)


@cirelation.route("/<int:first_ci>/second_cis", methods=["GET"])
def get_second_cis_by_first_ci(first_ci=None):
    page = get_page(request.values.get("page", 1))
    count = get_per_page(request.values.get("count"))
    relation_type = request.values.get("relation_type", "contain")
    manager = CIRelationManager()
    numfound, total, second_cis = manager.get_second_cis(
        first_ci, page=page, per_page=count, relation_type=relation_type)
    return jsonify(numfound=numfound, total=total,
                   page=page, second_cis=second_cis)


@cirelation.route("/<int:second_ci>/first_cis", methods=["GET"])
def get_first_cis_by_second_ci(second_ci=None):
    page = get_page(request.values.get("page", 1))
    count = get_per_page(request.values.get("count"))
    relation_type = request.values.get("relation_type", "contain")

    manager = CIRelationManager()
    numfound, total, first_cis = manager.get_first_cis(
        second_ci, per_page=count, page=page, relation_type=relation_type)
    return jsonify(numfound=numfound, total=total,
                   page=page, first_cis=first_cis)


@cirelation.route("/<int:first_ci>/<int:second_ci>", methods=["POST"])
@auth_with_key
def create_ci_relation(first_ci=None, second_ci=None):
    relation_type = request.values.get("relation_type", "contain")
    manager = CIRelationManager()
    res = manager.add(first_ci, second_ci, relation_type=relation_type)
    return jsonify(cr_id=res)


@cirelation.route("/<int:cr_id>", methods=["DELETE"])
@auth_with_key
def delete_ci_relation(cr_id=None):
    manager = CIRelationManager()
    manager.delete(cr_id)
    return jsonify(message="CIType Relation is deleted")


@cirelation.route("/<int:first_ci>/<int:second_ci>", methods=["DELETE"])
@auth_with_key
def delete_ci_relation_2(first_ci, second_ci):
    manager = CIRelationManager()
    manager.delete_2(first_ci, second_ci)
    return jsonify(message="CIType Relation is deleted")