# -*- coding:utf-8 -*- 


from flask import Blueprint
from flask import jsonify


special = Blueprint(__name__, "special")


@special.route("/api/v0.1/special", methods=["GET"])
def index():
    """
    定义专用接口
    """
    return jsonify(code=200)