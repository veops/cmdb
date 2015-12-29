# -*- coding:utf-8 -*- 


import time
from functools import wraps

from flask import request
from flask import render_template
from flask import current_app

from lib.exception import InvalidUsageError


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def argument_required1(*args_required):
    from manage import InvalidUsageError

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for arg in args_required:
                if request.values.get(arg, None) is None:
                    raise InvalidUsageError(
                        "argument {0} is required".format(arg), 400)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


class argument_required(object):
    def __init__(self, *args):
        self.args = args

    def __enter__(self):
        for arg in self.args:
            if not request.values.get(arg):
                raise InvalidUsageError(
                    "argument {0} is required".format(arg), status_code=400)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def url_statistic(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        start = time.time()
        r = f(*args, **kwargs)
        spend = time.time() - start
        url = request.path
        current_app.logger.info(url)
        current_app.logger.info(spend)
        return r
    return decorated_func