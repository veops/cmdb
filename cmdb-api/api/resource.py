# -*- coding:utf-8 -*-

import os
import sys
from inspect import getmembers
from inspect import isclass

import six
from flask import jsonify
from flask import send_file
from flask_restful import Resource

from api.lib.perm.auth import auth_required


class APIView(Resource):
    method_decorators = [auth_required]

    def __init__(self):
        super(APIView, self).__init__()

    @staticmethod
    def jsonify(*args, **kwargs):
        return jsonify(*args, **kwargs)

    @staticmethod
    def send_file(*args, **kwargs):
        return send_file(*args, **kwargs)


API_PACKAGE = os.path.abspath(os.path.dirname(__file__))


def register_resources(resource_path, rest_api):
    for root, _, files in os.walk(os.path.join(resource_path)):
        for filename in files:
            if not filename.startswith("_") and filename.endswith("py"):
                if root not in sys.path:
                    sys.path.insert(1, root)
                view = __import__(os.path.splitext(filename)[0])
                resource_list = [o[0] for o in getmembers(view) if isclass(o[1]) and issubclass(o[1], Resource)]
                resource_list = [i for i in resource_list if i != "APIView"]
                for resource_cls_name in resource_list:
                    resource_cls = getattr(view, resource_cls_name)
                    if not hasattr(resource_cls, "url_prefix"):
                        resource_cls.url_prefix = ("",)
                    if isinstance(resource_cls.url_prefix, six.string_types):
                        resource_cls.url_prefix = (resource_cls.url_prefix,)
                    rest_api.add_resource(resource_cls, *resource_cls.url_prefix)
