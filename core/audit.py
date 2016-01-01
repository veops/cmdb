# -*- coding:utf-8 -*- 

__author__ = 'pycook'

import urllib

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

from lib.audit import CIAuditManager
from lib.utils import get_page
from lib.auth import auth_with_key


audit = Blueprint("audit", __name__)


@audit.route("", methods=["GET"])
def get_ci_audits():
    page = get_page(request.values.get("page", 1))
    type_ids = request.values.get("type_ids", "").split(",")
    type_ids = map(int, filter(lambda x: x != "", type_ids))
    type_ids = tuple(type_ids)
    numfound, total, ci_audits = CIAuditManager().get_cis_for_audits(
        page, type_ids)
    return jsonify(numfound=numfound, total=total,
                   page=page, ci_audits=ci_audits)


@audit.route("", methods=["POST"])
@auth_with_key
def create_ci_audit():
    if request.data:
        args = dict()
        _args = request.data.split("&")
        for arg in _args:
            if arg:
                args[arg.split("=")[0]] = \
                    urllib.unquote(urllib.unquote(arg.split("=")[1]))
    else:
        args = request.values
    attr_pairs = dict()
    type_name = ""
    for k, v in args.items():
        if k == "ci_type":
            type_name = v
        elif not k.startswith("_"):
            attr_pairs[k] = v
    ret, res = CIAuditManager().create_ci_audits(type_name=type_name,
                                                 attr_pairs=attr_pairs)
    if not ret:
        return abort(500, res)
    return jsonify(code=200)


@audit.route("/attribute/<int:audit_id>", methods=["POST"])
@auth_with_key
def audit_by_attr(audit_id):
    attr_ids = request.values.get("attr_ids", "")
    if not attr_ids:
        return abort(500, "argument attr_ids is required")
    split_tag = filter(lambda x: x in attr_ids, [";", ","])
    attr_value = None
    if not split_tag:
        attr_value = request.values.get("attr_value")
        if attr_value is None:
            return abort(500, "argument attr_value is required")
        attr_ids = [int(attr_ids)]
    else:
        attr_ids = attr_ids.split(split_tag[0])
        attr_ids = map(int, attr_ids)

    manager = CIAuditManager()
    ret, res = manager.audit_by_attr(audit_id, attr_ids, value=attr_value)
    if ret:
        return jsonify(code=200)
    else:
        return abort(500, res)


@audit.route("/cis", methods=["POST"])
@auth_with_key
def audit_by_cis():
    ci_ids = request.values.get("ci_ids", "")
    if not ci_ids:
        return abort(500, "argument ci_ids is required")
    split_tag = filter(lambda x: x in ci_ids, [",", ";"])
    if split_tag:
        ci_ids = ci_ids.split(split_tag[0])
    else:
        ci_ids = [ci_ids]
    ci_ids = map(int, ci_ids)
    manager = CIAuditManager()
    ret, res = manager.audit_by_cis(ci_ids)
    if ret:
        return jsonify(code=200)
    else:
        return abort(500, res)