# -*- coding:utf-8 -*-

import json

import requests
from flask import current_app
from jinja2 import Template
from markdownify import markdownify as md

from api.lib.mail import send_mail


def _request_messenger(subject, body, tos, sender, payload):
    params = dict(sender=sender, title=subject,
                  tos=[to[sender] for to in tos if to.get(sender)])

    if not params['tos']:
        raise Exception("no receivers")

    params['tos'] = [Template(i).render(payload) for i in params['tos'] if i.strip()]

    if sender == "email":
        params['msgtype'] = 'text/html'
        params['content'] = body
    else:
        params['msgtype'] = 'markdown'
        try:
            content = md("{}\n{}".format(subject or '', body or ''))
        except Exception as e:
            current_app.logger.warning("html2markdown failed: {}".format(e))
            content = "{}\n{}".format(subject or '', body or '')

        params['content'] = json.dumps(dict(content=content))

    resp = requests.post(current_app.config.get('MESSENGER_URL'), json=params)
    if resp.status_code != 200:
        raise Exception(resp.text)

    return resp.text


def notify_send(subject, body, methods, tos, payload=None):
    payload = payload or {}
    payload = {k: v or '' for k, v in payload.items()}
    subject = Template(subject).render(payload)
    body = Template(body).render(payload)

    res = ''
    for method in methods:
        if method == "email" and not current_app.config.get('USE_MESSENGER', True):
            send_mail(None, [Template(to.get('email')).render(payload) for to in tos], subject, body)

        res += (_request_messenger(subject, body, tos, method, payload) + "\n")

    return res
