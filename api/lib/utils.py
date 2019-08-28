# -*- coding:utf-8 -*- 

import six
import redis
from flask import current_app


def get_page(page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    return page if page >= 1 else 1


def get_page_size(page_size):
    if page_size == "all":
        return page_size

    try:
        page_size = int(page_size)
    except (ValueError, TypeError):
        page_size = current_app.config.get("DEFAULT_PAGE_COUNT")
    return page_size if page_size >= 1 else current_app.config.get("DEFAULT_PAGE_COUNT")


def handle_arg_list(arg):
    return list(filter(lambda x: x != "", arg.strip().split(","))) if isinstance(arg, six.string_types) else arg


class RedisHandler(object):
    def __init__(self, flask_app=None, prefix=None):
        self.flask_app = flask_app
        self.prefix = prefix
        self.r = None

    def init_app(self, app):
        self.flask_app = app
        config = self.flask_app.config
        try:
            pool = redis.ConnectionPool(
                max_connections=config.get("REDIS_MAX_CONN"),
                host=config.get("CACHE_REDIS_HOST"),
                port=config.get("CACHE_REDIS_PORT"),
                db=config.get("REDIS_DB"))
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            current_app.logger.warning(str(e))
            current_app.logger.error("init redis connection failed")

    def get(self, key_ids):
        try:
            value = self.r.hmget(self.prefix, key_ids)
        except Exception as e:
            current_app.logger.error("get redis error, %s" % str(e))
            return
        return value

    def _set(self, obj):
        try:
            self.r.hmset(self.prefix, obj)
        except Exception as e:
            current_app.logger.error("set redis error, %s" % str(e))

    def add(self, obj):
        self._set(obj)

    def delete(self, key_id):
        try:
            ret = self.r.hdel(self.prefix, key_id)
            if not ret:
                current_app.logger.warn("[%d] is not in redis" % key_id)
        except Exception as e:
            current_app.logger.error("delete redis key error, %s" % str(e))
