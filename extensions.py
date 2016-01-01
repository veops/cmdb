# -*- coding: utf-8 -*-


from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.celery import Celery

from lib.utils import RedisHandler


__all__ = ['mail', 'db', 'cache', 'celery', "rd"]


mail = Mail()
db = SQLAlchemy()
cache = Cache()
celery = Celery()
rd = RedisHandler()