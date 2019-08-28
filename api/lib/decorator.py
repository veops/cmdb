# -*- coding:utf-8 -*-


from functools import wraps

from flask import abort
from flask import request


def kwargs_required(*required_args):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in required_args:
                if arg not in kwargs:
                    return abort(400, "Argument <{0}> is required".format(arg))
            return func(*args, **kwargs)

        return wrapper

    return decorate


def args_required(*required_args):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in required_args:
                if arg not in request.values:
                    return abort(400, "Argument <{0}> is required".format(arg))
            return func(*args, **kwargs)

        return wrapper

    return decorate
