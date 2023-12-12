# -*- coding:utf-8 -*-

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
from flask_login import login_user, logout_user
from six.moves.urllib.parse import urlencode

from api.lib.perm.acl.cache import UserCache

blueprint = Blueprint('oidc', __name__)


@blueprint.route('/api/oidc/login')
@blueprint.route('/api/sso/login')
def login():
    if request.values.get("next"):
        session["next"] = request.values.get("next")

    session['oidc_state'] = secrets.token_urlsafe(16)

    qs = urlencode({
        'client_id': current_app.config['OIDC_CLIENT_ID'],
        'redirect_uri': url_for('oidc.callback', _external=True),
        'response_type': current_app.config['OIDC_RESPONSE_TYPE'],
        'scope': ' '.join(current_app.config['OIDC_SCOPES'] or []),
        'state': session['oidc_state'],
    })

    return redirect("{}?{}".format(current_app.config['OIDC_AUTHORIZE_URL'].split('?')[0], qs))


@blueprint.route('/api/oidc/callback')
def callback():
    redirect_url = session.get("next") or current_app.config.get("OIDC_AFTER_LOGIN")

    if request.values['state'] != session.get('oidc_state'):
        return abort(401, "state is invalid")

    if 'code' not in request.values:
        return abort(401, 'code is invalid')

    response = requests.post(current_app.config['OIDC_TOKEN_URL'], data={
        'client_id': current_app.config['OIDC_CLIENT_ID'],
        'client_secret': current_app.config['OIDC_CLIENT_SECRET'],
        'code': request.values['code'],
        'grant_type': current_app.config['OIDC_GRANT_TYPE'],
        'redirect_uri': url_for('oidc.callback', _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        current_app.logger.error(response.text)
        return abort(401)
    oidc_token = response.json().get('access_token')
    if not oidc_token:
        return abort(401)

    response = requests.get(current_app.config['OIDC_USER_INFO']['url'], headers={
        'Authorization': 'Bearer {}'.format(oidc_token),
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        return abort(401)

    email = current_app.config['OIDC_USER_INFO']['email'](response.json())
    username = current_app.config['OIDC_USER_INFO']['username'](response.json())
    user = UserCache.get(username)
    if user is None:
        current_app.logger.info("create user: {}".format(username))
        from api.lib.perm.acl.user import UserCRUD

        user_dict = dict(username=username, email=email)
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

    return redirect(redirect_url)


@blueprint.route('/api/oidc/logout')
@blueprint.route('/api/sso/logout')
def logout():
    "acl" in session and session.pop("acl")
    "uid" in session and session.pop("uid")
    'oidc_state' in session and session.pop('oidc_state')
    "next" in session and session.pop("next")

    redirect_url = url_for('oidc.login', _external=True, next=request.referrer)

    logout_user()

    current_app.logger.debug('Redirecting to: {0}'.format(redirect_url))

    return redirect(redirect_url)
