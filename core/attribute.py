# -*- coding:utf-8 -*- 


from flask import jsonify
from flask import request
from flask import Blueprint
from flask import abort
from flask import current_app

from lib.attribute import AttributeManager
from lib.ci_type import CITypeAttributeManager
from lib.decorator import argument_required
from lib.exception import InvalidUsageError
from lib.auth import auth_with_key

attribute = Blueprint("attribute", __name__)


@attribute.route("", methods=["GET"])
def get_attributes():
    q = request.values.get("q")
    attrs = AttributeManager().get_attributes(name=q)
    count = len(attrs)
    return jsonify(numfound=count, attributes=attrs)


@attribute.route("/<string:attr_name>", methods=["GET"])
@attribute.route("/<int:attr_id>", methods=["GET"])
def get_attribute(attr_name=None, attr_id=None):
    attr_manager = AttributeManager()
    attr_dict = None
    if attr_name is not None:
        attr_dict = attr_manager.get_attribute_by_name(attr_name)
        if attr_dict is None:
            attr_dict = attr_manager.get_attribute_by_alias(attr_name)
    elif attr_id is not None:
        attr_dict = attr_manager.get_attribute_by_id(attr_id)
    if attr_dict is not None:
        return jsonify(attribute=attr_dict)
    abort(404, "attribute not found")


@attribute.route("", methods=["POST"])
@auth_with_key
def create_attribute():
    with argument_required("attr_name"):
        attr_name = request.values.get("attr_name")
        current_app.logger.info(attr_name)
        attr_alias = request.values.get("attr_alias", attr_name)
        choice_value = request.values.get("choice_value")
        is_multivalue = request.values.get("is_multivalue", False)
        is_uniq = request.values.get("is_uniq", False)
        is_index = request.values.get("is_index", False)
        value_type = request.values.get("value_type", "text")
        try:
            is_multivalue = int(is_multivalue)
            is_uniq = int(is_uniq)
            is_index = int(is_index)
        except ValueError:
            raise InvalidUsageError("argument format is error")
        attr_manager = AttributeManager()
        kwargs = {"choice_value": choice_value, "is_multivalue": is_multivalue,
                  "is_uniq": is_uniq, "value_type": value_type,
                  "is_index": is_index}
        ret, res = attr_manager.add(attr_name, attr_alias, **kwargs)
        if not ret:
            return abort(500, res)
        return jsonify(attr_id=res)


@attribute.route("/<int:attr_id>", methods=["PUT"])
@auth_with_key
def update_attribute(attr_id=None):
    with argument_required("attr_name"):
        attr_name = request.values.get("attr_name")
        attr_alias = request.values.get("attr_alias", attr_name)
        choice_value = request.values.get("choice_value")
        is_multivalue = request.values.get("is_multivalue", False)
        is_uniq = request.values.get("is_uniq", False)
        value_type = request.values.get("value_type", "text")
        try:
            is_multivalue = int(is_multivalue)
            is_uniq = int(is_uniq)
        except ValueError:
            raise InvalidUsageError("argument format is error")
        attr_manager = AttributeManager()
        kwargs = {"choice_value": choice_value, "is_multivalue": is_multivalue,
                  "is_uniq": is_uniq, "value_type": value_type}
        ret, res = attr_manager.update(attr_id, attr_name,
                                       attr_alias, **kwargs)
        if not ret:
            return abort(500, res)
        return jsonify(attr_id=res)


@attribute.route("/<int:attr_id>", methods=["DELETE"])
@auth_with_key
def delete_attribute(attr_id=None):
    attr_manager = AttributeManager()
    res = attr_manager.delete(attr_id)
    return jsonify(message="attribute {0} deleted".format(res))


@attribute.route("/citype/<int:type_id>", methods=["GET"])
def get_attributes_by_type(type_id=None):
    manager = CITypeAttributeManager()
    from models.cmdb import CITypeCache, CIAttributeCache

    t = CITypeCache.get(type_id)
    if not t:
        return abort(400, "CIType {0} is not existed".format(type_id))
    uniq_id = t.uniq_id
    unique = CIAttributeCache.get(uniq_id).attr_name
    return jsonify(attributes=manager.get_attributes_by_type_id(type_id),
                   type_id=type_id, uniq_id=uniq_id, unique=unique)


@attribute.route("/citype/<int:type_id>", methods=["POST"])
@auth_with_key
def create_attributes_to_citype(type_id=None):
    with argument_required("attr_id"):
        attr_ids = request.values.get("attr_id", "")
        is_required = request.values.get("is_required", False)
        attr_id_list = attr_ids.strip().split(",")
        if "" in attr_id_list:
            attr_id_list.remove("")
        attr_id_list = map(int, attr_id_list)
        try:
            is_required = int(is_required)
        except ValueError:
            abort(500, "argument format is error")
        manager = CITypeAttributeManager()
        manager.add(type_id, attr_id_list, is_required=is_required)
        return jsonify(attributes=attr_id_list)


@attribute.route("/citype/<int:type_id>", methods=["DELETE"])
@auth_with_key
def delete_attribute_in_type(type_id=None):
    with argument_required("attr_id"):
        attr_ids = request.values.get("attr_id", "")
        attr_id_list = attr_ids.strip().split(",")
        manager = CITypeAttributeManager()
        manager.delete(type_id, attr_id_list)
        return jsonify(attributes=attr_id_list)