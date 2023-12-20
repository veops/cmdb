# -*- coding:utf-8 -*-
import datetime
import uuid

import bs4
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from six.moves.urllib.parse import urlparse
from six.moves.urllib_request import urlopen

from api.lib.common_setting.common_data import AuthenticateDataCRUD
from api.lib.common_setting.const import AuthenticateType
from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.cache import UserCache
from api.lib.perm.acl.resp_format import ErrFormat
from .cas_urls import create_cas_login_url
from .cas_urls import create_cas_logout_url
from .cas_urls import create_cas_validate_url

blueprint = Blueprint('cas', __name__)


@blueprint.route('/api/cas/login')
@blueprint.route('/api/sso/login')
def login():
    """
    This route has two purposes. First, it is used by the user
    to login. Second, it is used by the CAS to respond with the
    `ticket` after the user logs in successfully.

    When the user accesses this url, they are redirected to the CAS
    to login. If the login was successful, the CAS will respond to this
    route with the ticket in the url. The ticket is then validated.
    If validation was successful the logged in username is saved in
    the user's session under the key `CAS_USERNAME_SESSION_KEY`.
    """
    config = AuthenticateDataCRUD(AuthenticateType.CAS).get()

    cas_token_session_key = current_app.config['CAS_TOKEN_SESSION_KEY']
    if request.values.get("next"):
        session["next"] = request.values.get("next")

    # _service = url_for('cas.login', _external=True)
    _service = "{}://{}{}".format(urlparse(request.referrer).scheme,
                                  urlparse(request.referrer).netloc,
                                  url_for('cas.login'))

    redirect_url = create_cas_login_url(
        config['cas_server'],
        config['cas_login_route'],
        _service)

    if 'ticket' in request.args:
        session[cas_token_session_key] = request.args.get('ticket')

    if request.args.get('ticket'):

        if validate(request.args['ticket']):
            redirect_url = session.get("next") or config.get("cas_after_login") or "/"
            username = session.get("CAS_USERNAME")
            user = UserCache.get(username)
            login_user(user)

            session.permanent = True

            _id = AuditCRUD.add_login_log(username, True, ErrFormat.login_succeed)
            session['LOGIN_ID'] = _id

        else:
            del session[cas_token_session_key]
            redirect_url = create_cas_login_url(
                config['cas_server'],
                config['cas_login_route'],
                url_for('cas.login', _external=True),
                renew=True)

            AuditCRUD.add_login_log(session.get("CAS_USERNAME"), False, ErrFormat.invalid_password)

    current_app.logger.info("redirect to: {0}".format(redirect_url))
    return redirect(redirect_url)


@blueprint.route('/api/cas/logout')
@blueprint.route('/api/sso/logout')
def logout():
    """
    When the user accesses this route they are logged out.
    """
    config = AuthenticateDataCRUD(AuthenticateType.CAS).get()
    current_app.logger.info(config)

    cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']
    cas_token_session_key = current_app.config['CAS_TOKEN_SESSION_KEY']

    cas_username_session_key in session and session.pop(cas_username_session_key)
    "acl" in session and session.pop("acl")
    "uid" in session and session.pop("uid")
    cas_token_session_key in session and session.pop(cas_token_session_key)
    "next" in session and session.pop("next")

    redirect_url = create_cas_logout_url(
        config['cas_server'],
        config['cas_logout_route'],
        url_for('cas.login', _external=True, next=request.referrer))

    logout_user()

    AuditCRUD.add_login_log(None, None, None, _id=session.get('LOGIN_ID'), logout_at=datetime.datetime.now())

    current_app.logger.debug('Redirecting to: {0}'.format(redirect_url))

    return redirect(redirect_url)


def validate(ticket):
    """
    Will attempt to validate the ticket. If validation fails, then False
    is returned. If validation is successful, then True is returned
    and the validated username is saved in the session under the
    key `CAS_USERNAME_SESSION_KEY`.
    """
    config = AuthenticateDataCRUD(AuthenticateType.CAS).get()

    cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']

    current_app.logger.debug("validating token {0}".format(ticket))

    cas_validate_url = create_cas_validate_url(
        config['cas_validate_server'],
        config['cas_validate_route'],
        url_for('cas.login', _external=True),
        ticket)

    current_app.logger.debug("Making GET request to {0}".format(cas_validate_url))

    try:
        response = urlopen(cas_validate_url).read()
        ticket_id = _parse_tag(response, "cas:user")
        strs = [s.strip() for s in ticket_id.split('|') if s.strip()]
        username, is_valid = None, False
        if len(strs) == 1:
            username = strs[0]
            is_valid = True
    except ValueError:
        current_app.logger.error("CAS returned unexpected result")
        is_valid = False
        return is_valid

    if is_valid:
        current_app.logger.debug("{}: {}".format(cas_username_session_key, username))
        session[cas_username_session_key] = username
        user = UserCache.get(username)
        if user is None:
            current_app.logger.info("create user: {}".format(username))
            from api.lib.perm.acl.user import UserCRUD
            soup = bs4.BeautifulSoup(response)
            cas_user_map = config.get('cas_user_map')
            user_dict = dict()
            for k in cas_user_map:
                v = soup.find(cas_user_map[k]['tag'], cas_user_map[k].get('attrs', {}))
                user_dict[k] = v and v.text or None
            user_dict['password'] = uuid.uuid4().hex
            if "email" not in user_dict:
                user_dict['email'] = username

            UserCRUD.add(**user_dict)

        from api.lib.perm.acl.acl import ACLManager
        user_info = ACLManager.get_user_info(username)

        session["acl"] = dict(uid=user_info.get("uid"),
                              avatar=user.avatar if user else user_info.get("avatar"),
                              userId=user_info.get("uid"),
                              rid=user_info.get("rid"),
                              userName=user_info.get("username"),
                              nickName=user_info.get("nickname"),
                              parentRoles=user_info.get("parents"),
                              childRoles=user_info.get("children"),
                              roleName=user_info.get("role"))
        session["uid"] = user_info.get("uid")
        current_app.logger.debug(session)
        current_app.logger.debug(request.url)
    else:
        current_app.logger.debug("invalid")

    return is_valid


def _parse_tag(string, tag):
    """
    Used for parsing xml.  Search string for the first occurence of
    <tag>.....</tag> and return text (stripped of leading and tailing
    whitespace) between tags.  Return "" if tag not found.
    """
    soup = bs4.BeautifulSoup(string)

    if soup.find(tag) is None:
        return ''

    return soup.find(tag).string.strip()
