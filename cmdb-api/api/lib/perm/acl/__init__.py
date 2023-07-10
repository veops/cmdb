# -*- coding:utf-8 -*-


from functools import wraps

from flask import abort
from flask import request

from api.lib.perm.acl.cache import AppCache, AppAccessTokenCache
from api.lib.perm.acl.resp_format import ErrFormat


def validate_app(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get('App-Access-Token', '').strip():
            app_id = request.values.get('app_id')
            app = AppCache.get(app_id)
            if app is None:
                return abort(400, ErrFormat.app_not_found.format("id={}".format(app_id)))
            request.values['app_id'] = app.id

        return func(*args, **kwargs)

    return wrapper
