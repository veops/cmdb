# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import SMTPHandler
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask import request
from flask import g
from flask.ext.babel import Babel
from flask.ext.principal import identity_loaded
from flask.ext.principal import Principal

import core
from extensions import db
from extensions import mail
from extensions import cache
from extensions import celery
from extensions import rd
from models.account import User
from lib.template import filters


APP_NAME = "CMDB-API"

MODULES = (
    (core.attribute, "/api/v0.1/attributes"),
    (core.citype, "/api/v0.1/citypes"),
    (core.cityperelation, "/api/v0.1/cityperelations"),
    (core.cirelation, "/api/v0.1/cirelations"),
    (core.ci, "/api/v0.1/ci"),
    (core.history, "/api/v0.1/history"),
    (core.account, "/api/v0.1/accounts"),
    # (core.special, ""),
)


def make_app(config=None, modules=None):
    if not modules:
        modules = MODULES
    app = Flask(APP_NAME)
    app.config.from_pyfile(config)
    configure_extensions(app)
    configure_i18n(app)
    configure_identity(app)
    configure_blueprints(app, modules)
    configure_logging(app)
    configure_template_filters(app)
    return app


def configure_extensions(app):
    db.app = app
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    celery.init_app(app)
    rd.init_app(app)


def configure_i18n(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES', ['en', 'zh'])
        return request.accept_languages.best_match(accept_languages)


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)


def configure_blueprints(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


def configure_identity(app):
    principal = Principal(app)
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_logging(app):
    hostname = os.uname()[1]
    mail_handler = SMTPHandler(
        app.config['MAIL_SERVER'],
        app.config['DEFAULT_MAIL_SENDER'],
        app.config['ADMINS'],
        '[%s] CMDB API error' % hostname,
        (
            app.config['MAIL_USERNAME'],
            app.config['MAIL_PASSWORD'],
        )
    )
    mail_formater = logging.Formatter(
        "%(asctime)s %(levelname)s %(pathname)s %(lineno)d\n%(message)s")
    mail_handler.setFormatter(mail_formater)
    mail_handler.setLevel(logging.ERROR)
    if not app.debug:
        app.logger.addHandler(mail_handler)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s")
    log_file = app.config['LOG_PATH']
    file_handler = TimedRotatingFileHandler(
        log_file, when='d', interval=1, backupCount=7)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))


def configure_template_filters(app):
    for name in dir(filters):
        if callable(getattr(filters, name)):
            app.add_template_filter(getattr(filters, name))
