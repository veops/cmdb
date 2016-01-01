# -*- coding:utf-8 -*-


import redis

from flask import current_app


class RedisHandler(object):
    def __init__(self):
        config = current_app.config
        try:
            pool = redis.ConnectionPool(
                max_connections=config.get("REDIS_MAX_CONN"),
                host=config.get("CACHE_REDIS_HOST"),
                port=config.get("CACHE_REDIS_PORT"),
                db=config.get("REDIS_DB"))
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            print e
            current_app.logger.error("init redis connection failed")

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get(self, ci_ids, key="CMDB_CI"):
        try:
            value = self.r.hmget(key, ci_ids)
        except Exception as e:
            current_app.logger.error("get redis error, %s" % str(e))
            return
        return value

    def _set(self, ci, key="CMDB_CI"):
        try:
            self.r.hmset(key, ci)
        except Exception as e:
            current_app.logger.error("set redis error, %s" % str(e))

    def add(self, ci):
        self._set(ci)

    def delete(self, ci_id, key="CMDB_CI"):
        try:
            ret = self.r.hdel(key, ci_id)
            if not ret:
                current_app.logger.warn("ci [%d] is not in redis" % ci_id)
        except Exception as e:
            current_app.logger.error("delete redis key error, %s" % str(e))

rd = RedisHandler.instance()


def get_page(page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page < 1:
        page = 1
    return page


def get_per_page(per_page):
    try:
        per_page = int(per_page)
    except:
        per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
    if per_page < 1:
        per_page = current_app.config.get("DEFAULT_PAGE_COUNT")
    return per_page