# -*- coding:utf-8 -*-

import json

import requests
from flask import current_app
from jinja2 import Template

from api.lib.mail import send_mail


def _request_messenger(subject, body, tos, sender):
    params = dict(sender=sender, title=subject,
                  tos=[to[sender] for to in tos if to.get(sender)])

    if not params['tos']:
        raise Exception("no receivers")

    if sender == "email":
        params['msgtype'] = 'text/html'
        params['content'] = body
    else:
        params['msgtype'] = 'text'
        params['content'] = json.dumps(dict(content=subject or body))

    resp = requests.post(current_app.config.get('MESSENGER_URL'), json=params)
    if resp.status_code != 200:
        raise Exception(resp.text)

    return resp.text


def notify_send(subject, body, methods, tos, payload=None):
    payload = payload or {}
    subject = Template(subject).render(payload)
    body = Template(body).render(payload)

    res = ''
    for method in methods:
        if method == "email" and not current_app.config.get('USE_MESSENGER', True):
            send_mail(None, [to.get('email') for to in tos], subject, body)

        res += _request_messenger(subject, body, tos, method) + "\n"

    return res
