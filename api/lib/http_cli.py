# -*- coding:utf-8 -*-


import hashlib

import requests
from flask import abort
from flask import current_app
from flask import g
from future.moves.urllib.parse import urlparse


def build_api_key(path, params):
    g.user is not None or abort(403, u"您得登陆才能进行该操作")
    key = g.user.key
    secret = g.user.secret
    values = "".join([str(params[k]) for k in sorted(params.keys())
                      if params[k] is not None]) if params.keys() else ""
    _secret = "".join([path, secret, values]).encode("utf-8")
    params["_secret"] = hashlib.sha1(_secret).hexdigest()
    params["_key"] = key
    return params


def api_request(url, method="get", params=None, ret_key=None):
    params = params or {}
    resp = None
    try:
        method = method.lower()
        params = build_api_key(urlparse(url).path, params)
        if method == "get":
            resp = getattr(requests, method)(url, params=params)
        else:
            resp = getattr(requests, method)(url, data=params)
        if resp.status_code != 200:
            return abort(resp.status_code, resp.json().get("message"))
        resp = resp.json()
        if ret_key is not None:
            return resp.get(ret_key)
        return resp
    except Exception as e:
        code = e.code if hasattr(e, "code") else None
        if isinstance(code, int) and resp is not None:
            return abort(code, resp.json().get("message"))
        current_app.logger.warning(url)
        current_app.logger.warning(params)
        current_app.logger.error(str(e))
        return abort(500, "server unknown error")
