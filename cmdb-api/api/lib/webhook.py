# -*- coding:utf-8 -*-

import json
from functools import partial

import requests
from jinja2 import Template
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer {}".format(self.token)
        return r


def _wrap_auth(**kwargs):
    auth_type = (kwargs.get('type') or "").lower()
    if auth_type == "basicauth":
        return HTTPBasicAuth(kwargs.get('username'), kwargs.get('password'))

    elif auth_type == "bearer":
        return BearerAuth(kwargs.get('token'))

    elif auth_type == 'oauth2.0':
        client_id = kwargs.get('client_id')
        client_secret = kwargs.get('client_secret')
        authorization_base_url = kwargs.get('authorization_base_url')
        token_url = kwargs.get('token_url')
        redirect_url = kwargs.get('redirect_url')
        scope = kwargs.get('scope')

        oauth2_session = OAuth2Session(client_id, scope=scope or None)
        oauth2_session.authorization_url(authorization_base_url)

        oauth2_session.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_url)

        return oauth2_session

    elif auth_type == "apikey":
        return HTTPBasicAuth(kwargs.get('key'), kwargs.get('value'))


def webhook_request(webhook, payload):
    """

    :param webhook:
    {
        "url": "https://veops.cn"
        "method": "GET|POST|PUT|DELETE"
        "body": {},
        "headers": {
            "Content-Type": "Application/json"
        },
        "parameters": {
            "key": "value"
        },
        "authorization": {
            "type": "BasicAuth|Bearer|OAuth2.0|APIKey",
            "password": "mmmm",  # BasicAuth
            "username": "bbb",   # BasicAuth

            "token": "xxx",  # Bearer

            "key": "xxx",    # APIKey
            "value": "xxx",  # APIKey

            "client_id": "xxx",               # OAuth2.0
            "client_secret": "xxx",           # OAuth2.0
            "authorization_base_url": "xxx",  # OAuth2.0
            "token_url": "xxx",               # OAuth2.0
            "redirect_url": "xxx",            # OAuth2.0
            "scope": "xxx"                    # OAuth2.0
        }
    }
    :param payload:
    :return:
    """
    assert webhook.get('url') is not None

    payload = {k: v or '' for k, v in payload.items()}

    url = Template(webhook['url']).render(payload)

    params = webhook.get('parameters') or None
    if isinstance(params, dict):
        params = json.loads(Template(json.dumps(params)).render(payload))

    headers = json.loads(Template(json.dumps(webhook.get('headers') or {})).render(payload))

    data = Template(json.dumps(webhook.get('body', ''))).render(payload)
    auth = _wrap_auth(**webhook.get('authorization', {}))

    if (webhook.get('authorization', {}).get("type") or '').lower() == 'oauth2.0':
        request = getattr(auth, webhook.get('method', 'GET').lower())
    else:
        request = partial(requests.request, webhook.get('method', 'GET'))

    return request(
        url,
        params=params,
        headers=headers or None,
        data=data,
        auth=auth
    )
