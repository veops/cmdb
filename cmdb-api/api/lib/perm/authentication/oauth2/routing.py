# -*- coding:utf-8 -*-

import datetime
import secrets
import uuid

import requests
from flask import Blueprint
from flask import abort
from flask import current_app
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import urlparse

from api.lib.common_setting.common_data import AuthenticateDataCRUD
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat

blueprint = Blueprint('oauth2', __name__)
OAUTH_HTTP_TIMEOUT = 5


def _safe_next_path(target):
    if not target:
        return None

    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or target.startswith('//') or not target.startswith('/'):
        return None

    return target


@blueprint.route('/api/<string:auth_type>/login')
def login(auth_type):
    config = AuthenticateDataCRUD(auth_type.upper()).get()

    next_path = _safe_next_path(request.values.get("next"))
    if next_path:
        session["next"] = next_path

    session[f'{auth_type}_state'] = secrets.token_urlsafe(16)

    auth_type = auth_type.upper()

    referrer = request.referrer or request.host_url
    redirect_uri = "{}://{}{}".format(urlparse(referrer).scheme,
                                      urlparse(referrer).netloc,
                                      url_for('oauth2.callback', auth_type=auth_type.lower()))
    qs = urlencode({
        'client_id': config['client_id'],
        'redirect_uri': redirect_uri,
        'response_type': current_app.config[f'{auth_type}_RESPONSE_TYPE'],
        'scope': ' '.join(config['scopes'] or []),
        'state': session[f'{auth_type.lower()}_state'],
    })

    return redirect("{}?{}".format(config['authorize_url'].split('?')[0], qs))


@blueprint.route('/api/<string:auth_type>/callback')
def callback(auth_type):
    auth_type = auth_type.upper()
    config = AuthenticateDataCRUD(auth_type).get()

    redirect_url = _safe_next_path(session.get("next")) or config.get('after_login') or '/'

    if request.values.get('state') != session.get(f'{auth_type.lower()}_state'):
        return abort(401, "state is invalid")

    if 'code' not in request.values:
        return abort(401, 'code is invalid')

    response = requests.post(config['token_url'], data={
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': request.values['code'],
        'grant_type': current_app.config[f'{auth_type}_GRANT_TYPE'],
        'redirect_uri': url_for('oauth2.callback', auth_type=auth_type.lower(), _external=True),
    }, headers={'Accept': 'application/json'}, timeout=OAUTH_HTTP_TIMEOUT)
    if response.status_code != 200:
        current_app.logger.error(response.text)
        return abort(401)
    access_token = response.json().get('access_token')
    if not access_token:
        return abort(401)

    response = requests.get(config['user_info']['url'], headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'Accept': 'application/json',
    }, timeout=OAUTH_HTTP_TIMEOUT)
    if response.status_code != 200:
        return abort(401)

    res = response.json()
    email = res.get(config['user_info']['email'])
    username = res.get(config['user_info']['username'])
    avatar = res.get(config['user_info'].get('avatar'))
    user = UserCache.get(username)
    if user is None:
        current_app.logger.info("create user: {}".format(username))
        from api.lib.perm.acl.user import UserCRUD

        user_dict = dict(username=username, email=email, avatar=avatar)
        user_dict['password'] = uuid.uuid4().hex

        user = UserCRUD.add(**user_dict)

    # log the user in
    login_user(user)

    from api.lib.perm.acl.acl import ACLManager
    user_info = ACLManager.get_user_info(username)

    session["acl"] = dict(uid=user_info.get("uid"),
                          avatar=user.avatar if user else user_info.get("avatar"),
                          userId=user_info.get("uid"),
                          rid=user_info.get("rid"),
                          userName=user_info.get("username"),
                          nickName=user_info.get("nickname") or user_info.get("username"),
                          parentRoles=user_info.get("parents"),
                          childRoles=user_info.get("children"),
                          roleName=user_info.get("role"))
    session["uid"] = user_info.get("uid")

    _id = AuditCRUD.add_login_log(username, True, ErrFormat.login_succeed)
    session['LOGIN_ID'] = _id

    return redirect(redirect_url)


@blueprint.route('/api/<string:auth_type>/logout')
def logout(auth_type):
    "acl" in session and session.pop("acl")
    "uid" in session and session.pop("uid")
    f'{auth_type}_state' in session and session.pop(f'{auth_type}_state')
    "next" in session and session.pop("next")

    redirect_url = url_for('oauth2.login', auth_type=auth_type, _external=True, next=request.referrer)

    logout_user()

    current_app.logger.debug('Redirecting to: {0}'.format(redirect_url))

    AuditCRUD.add_login_log(None, None, None, _id=session.get('LOGIN_ID'), logout_at=datetime.datetime.now())

    return redirect(redirect_url)
