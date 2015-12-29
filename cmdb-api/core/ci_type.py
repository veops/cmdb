# -*- coding:utf-8 -*- 


from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from lib.ci_type import CITypeManager
from lib.decorator import argument_required
from lib.auth import auth_with_key


citype = Blueprint("citype", __name__)


@citype.route("", methods=["GET"])
def get_citypes():
    type_name = request.args.get("type_name")
    manager = CITypeManager()
    citypes = manager.get_citypes(type_name)
    count = len(citypes)
    return jsonify(numfound=count, citypes=citypes)


@citype.route("/query", methods=["GET"])
def query():
    with argument_required("type"):
        _type = request.args.get("type")
        manager = CITypeManager()
        res = manager.query(_type)
        return jsonify(citype=res)


@citype.route("", methods=["POST"])
@auth_with_key
def create_citype():
    with argument_required("type_name"):
        type_name = request.values.get("type_name")
        type_alias = request.values.get("type_alias")
        if type_alias is None:
            type_alias = type_name
        _id = request.values.get("_id")
        unique = request.values.get("unique")
        enabled = request.values.get("enabled", True)
        icon_url = request.values.get("icon_url", "")
        manager = CITypeManager()
        ret, res = manager.add(type_name,  type_alias, _id=_id,
                               unique=unique, enabled=enabled,
                               icon_url=icon_url)
        if ret:
            return jsonify(type_id=res)
        abort(500, res)


@citype.route("/<int:type_id>", methods=["PUT"])
@auth_with_key
def update_citype(type_id=None):
    type_name = request.values.get("type_name")
    type_alias = request.values.get("type_alias")
    _id = request.values.get("_id")
    unique = request.values.get("unique")
    icon_url = request.values.get("icon_url")
    enabled = request.values.get("enabled")
    enabled = False if enabled in (0, "0") else True \
        if enabled is not None else None
    manager = CITypeManager()
    ret, res = manager.update(type_id, type_name, type_alias, _id=_id,
                              unique=unique, icon_url=icon_url,
                              enabled=enabled)
    if ret:
        return jsonify(type_id=type_id)
    abort(500, res)


@citype.route("/<int:type_id>", methods=["DELETE"])
@auth_with_key
def delete_citype(type_id=None):
    manager = CITypeManager()
    res = manager.delete(type_id)
    return jsonify(message=res)


@citype.route("/enable/<int:type_id>", methods=["GET", "POST"])
def enable(type_id=None):
    enable = request.values.get("enable", True)
    manager = CITypeManager()
    manager.set_enabled(type_id, enabled=enable)
    return jsonify(type_id=type_id)