# -*- coding:utf-8 -*-


from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery

from api.lib.utils import RedisHandler

bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
celery = Celery()
cors = CORS(supports_credentials=True)
rd = RedisHandler(prefix="CMDB_CI")  # TODO
