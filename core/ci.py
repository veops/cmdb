# -*- coding:utf-8 -*- 

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
import urllib

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import current_app
from flask import make_response
from flask import render_template
from flask import abort

from lib.auth import auth_with_key
from lib.ci import CIManager
from lib.ci import HostNumStatis
from lib.search import Search
from lib.search import SearchError
from lib.utils import get_page
from lib.utils import get_per_page
from models.ci_type import CITypeCache

ci = Blueprint("ci", __name__)


@ci.route("/type/<int:type_id>", methods=["GET"])
def get_cis_by_type(type_id=None):
    fields = request.args.get("fields", "").strip().split(",")
    fields = filter(lambda x: x != "", fields)

    ret_key = request.args.get("ret_key", "name")
    if ret_key not in ('name', 'alias', 'id'):
        ret_key = 'name'

    page = get_page(request.values.get("page", 1))
    count = get_per_page(request.values.get("count"))
    manager = CIManager()
    res = manager.get_cis_by_type(type_id, ret_key=ret_key,
                                  fields=fields, page=page, per_page=count)
    return jsonify(type_id=type_id, numfound=res[0],
                   total=len(res[2]), page=res[1], cis=res[2])


@ci.route("/<int:ci_id>", methods=['GET'])
def get_ci(ci_id=None):
    fields = request.args.get("fields", "").strip().split(",")
    fields = filter(lambda x: x != "", fields)

    ret_key = request.args.get("ret_key", "name")
    if ret_key not in ('name', 'alias', 'id'):
        ret_key = 'name'

    manager = CIManager()
    ci = manager.get_ci_by_id(ci_id, ret_key=ret_key, fields=fields)
    return jsonify(ci_id=ci_id, ci=ci)


@ci.route("/s", methods=["GET"])
@ci.route("/search", methods=["GET"])
def search():
    """@params: q: query statement
                fl: filter by column
                count: the number of ci
                ret_key: id, name, alias
                facet: statistic
                wt: result format
    """
    page = get_page(request.values.get("page", 1))
    count = get_per_page(request.values.get("count"))

    query = request.values.get('q', "")
    fl = request.values.get('fl', "").split(",")
    ret_key = request.values.get('ret_key', "name")
    if ret_key not in ('name', 'alias', 'id'):
        ret_key = 'name'
    facet = request.values.get("facet", "").split(",")
    wt = request.values.get('wt', 'json')
    fl = filter(lambda x: x != "", fl)
    facet = filter(lambda x: x != "", facet)
    sort = request.values.get("sort")

    start = time.time()
    s = Search(query, fl, facet, page, ret_key, count, sort)
    try:
        response, counter, total, page, numfound, facet = s.search()
    except SearchError, e:
        return abort(400, str(e))
    except Exception, e:
        current_app.logger.error(str(e))
        return abort(500, "search unknown error")

    if wt == 'xml':
        res = make_response(
            render_template("search.xml",
                            counter=counter,
                            total=total,
                            result=response,
                            page=page,
                            numfound=numfound,
                            facet=facet))
        res.headers['Content-type'] = 'text/xml'
        return res
    current_app.logger.debug("search time is :{0}".format(
        time.time() - start))
    return jsonify(numfound=numfound,
                   total=total,
                   page=page,
                   facet=facet,
                   counter=counter,
                   result=response)


@ci.route("", methods=["POST"])
@auth_with_key
def create_ci():
    ci_type = request.values.get("ci_type")
    _no_attribute_policy = request.values.get("_no_attribute_policy", "ignore")

    ci_dict = dict()
    for k, v in request.values.iteritems():
        if k != "ci_type" and not k.startswith("_"):
            ci_dict[k] = v.strip()

    manager = CIManager()
    current_app.logger.debug(ci_dict)
    ci_id = manager.add(ci_type, exist_policy="reject",
                        _no_attribute_policy=_no_attribute_policy, **ci_dict)
    return jsonify(ci_id=ci_id)


@ci.route("", methods=["PUT"])
@auth_with_key
def update_ci():
    if request.data:
        args = dict()
        _args = request.data.split("&")
        for arg in _args:
            if arg:
                args[arg.split("=")[0]] = \
                    urllib.unquote(urllib.unquote(arg.split("=")[1]))
    else:
        args = request.values

    ci_type = args.get("ci_type")
    _no_attribute_policy = args.get("_no_attribute_policy", "ignore")
    ci_dict = dict()
    for k, v in args.items():
        if k != "ci_type" and not k.startswith("_"):
            ci_dict[k] = v.strip()

    manager = CIManager()
    ci_id = manager.add(ci_type, exist_policy="replace",
                        _no_attribute_policy=_no_attribute_policy, **ci_dict)
    return jsonify(ci_id=ci_id)


@ci.route("/<int:ci_id>/unique", methods=["PUT"])
@auth_with_key
def update_ci_unique(ci_id):
    m = CIManager()
    m.update_unique_value(ci_id, request.values)
    return jsonify(ci_id=ci_id)


@ci.route("/<int:ci_id>", methods=["DELETE"])
@auth_with_key
def delete_ci(ci_id=None):
    manager = CIManager()
    manager.delete(ci_id)
    return jsonify(message="ok")


@ci.route("/heartbeat/<string:ci_type>/<string:unique>", methods=["POST"])
def add_heartbeat(ci_type, unique):
    if not unique or not ci_type:
        return jsonify(message="error")
    # return jsonify(message="ok")
    return jsonify(message=CIManager().add_heartbeat(ci_type, unique))


@ci.route("/heartbeat", methods=["GET"])
def get_heartbeat():
    page = get_page(request.values.get("page", 1))
    ci_type = request.values.get("ci_type", "").strip()
    try:
        ci_type = CITypeCache.get(ci_type).type_id
    except:
        return jsonify(numfound=0, result=[])
    agent_status = request.values.get("agent_status", None)
    if agent_status:
        agent_status = int(agent_status)
    numfound, result = CIManager().get_heartbeat(page,
                                                 ci_type,
                                                 agent_status=agent_status)
    return jsonify(numfound=numfound, result=result)


######################### just for frontend ###################################

@ci.route("/hosts/nums", methods=["GET"])
def get_hosts_nums():
    ci_type = request.args.get("ci_type", "").strip()
    ci_ids = request.args.get("ci_ids", "").strip()
    ci_id_list = ci_ids.split(",")
    ci_id_list = map(str, filter(lambda x: x != "", ci_id_list))
    res = {}
    if ci_type == "bu":
        res = HostNumStatis().get_hosts_by_bu(ci_id_list)
    elif ci_type == "product":
        res = HostNumStatis().get_hosts_by_product(ci_id_list)
    elif ci_type == "project":
        res = HostNumStatis().get_hosts_by_project(ci_id_list)
    return jsonify(hosts=res)