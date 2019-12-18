# -*- coding:utf-8 -*-


from functools import wraps

from flask import request
from flask import abort

from api.lib.perm.acl.cache import AppCache


def validate_app(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        app_id = request.values.get('app_id')
        app = AppCache.get(app_id)
        if app is None:
            return abort(400, "App <{0}> does not exist".format(app_id))
        request.values['app_id'] = app.id

        return func(*args, **kwargs)

    return wrapper
