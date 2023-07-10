# -*- coding:utf-8 -*- 

import base64
import json
import sys
import time
from typing import Set

import elasticsearch
import redis
import six
from Crypto.Cipher import AES
from elasticsearch import Elasticsearch
from flask import current_app


class BaseEnum(object):
    _ALL_ = set()  # type: Set[str]

    @classmethod
    def is_valid(cls, item):
        return item in cls.all()

    @classmethod
    def all(cls):
        if not cls._ALL_:
            cls._ALL_ = {
                getattr(cls, attr)
                for attr in dir(cls)
                if not attr.startswith("_") and not callable(getattr(cls, attr))
            }
        return cls._ALL_


def get_page(page):
    try:
        page = int(page)
    except (TypeError, ValueError):
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


def handle_bool_arg(arg):
    if arg in current_app.config.get("BOOL_TRUE"):
        return True
    return False


def handle_arg_list(arg):
    if isinstance(arg, (list, dict)):
        return arg

    if arg == 0:
        return [0]

    if not arg:
        return []

    if isinstance(arg, (six.integer_types, float)):
        return [arg]
    return list(filter(lambda x: x != "", arg.strip().split(","))) if isinstance(arg, six.string_types) else arg


class RedisHandler(object):
    def __init__(self, flask_app=None):
        self.flask_app = flask_app
        self.r = None

    def init_app(self, app):
        self.flask_app = app
        config = self.flask_app.config
        try:
            pool = redis.ConnectionPool(
                max_connections=config.get("REDIS_MAX_CONN"),
                host=config.get("CACHE_REDIS_HOST"),
                port=config.get("CACHE_REDIS_PORT"),
                password=config.get("CACHE_REDIS_PASSWORD"),
                db=config.get("REDIS_DB") or 0)
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            current_app.logger.warning(str(e))
            current_app.logger.error("init redis connection failed")

    def get(self, key_ids, prefix):
        try:
            value = self.r.hmget(prefix, key_ids)
        except Exception as e:
            current_app.logger.error("get redis error, {0}".format(str(e)))
            return
        return value

    def _set(self, obj, prefix):
        try:
            self.r.hmset(prefix, obj)
        except Exception as e:
            current_app.logger.error("set redis error, {0}".format(str(e)))

    def create_or_update(self, obj, prefix):
        self._set(obj, prefix)

    def delete(self, key_id, prefix):
        try:
            ret = self.r.hdel(prefix, key_id)
            if not ret:
                current_app.logger.warn("[{0}] is not in redis".format(key_id))
        except Exception as e:
            current_app.logger.error("delete redis key error, {0}".format(str(e)))


class ESHandler(object):
    def __init__(self, flask_app=None):
        self.flask_app = flask_app
        self.es = None
        self.index = "cmdb"

    def init_app(self, app):
        self.flask_app = app
        config = self.flask_app.config
        if config.get('ES_USER') and config.get('ES_PASSWORD'):
            uri = "http://{}:{}@{}:{}/".format(config.get('ES_USER'), config.get('ES_PASSWORD'),
                                               config.get('ES_HOST'), config.get('ES_PORT'))
        else:
            uri = "{}:{}".format(config.get('ES_HOST'), config.get('ES_PORT') or 9200)
        self.es = Elasticsearch(uri,
                                timeout=10,
                                max_retries=3,
                                retry_on_timeout=True,
                                retry_on_status=(502, 503, 504, "N/A"),
                                maxsize=10)
        try:
            if not self.es.indices.exists(index=self.index):
                self.es.indices.create(index=self.index)
        except elasticsearch.exceptions.RequestError as ex:
            if ex.error != 'resource_already_exists_exception':
                raise

    def update_mapping(self, field, value_type, other):
        body = {
            "properties": {
                field: {"type": value_type},
            }}
        body['properties'][field].update(other)

        self.es.indices.put_mapping(
            index=self.index,
            body=body
        )

    def get_index_id(self, ci_id):
        try:
            return self._get_index_id(ci_id)
        except:
            return self._get_index_id(ci_id)

    def _get_index_id(self, ci_id):
        query = {
            'query': {
                'match': {'ci_id': ci_id}
            },
        }
        res = self.es.search(index=self.index, body=query)
        if res['hits']['hits']:
            return res['hits']['hits'][-1].get('_id')

    def create(self, body):
        return self.es.index(index=self.index, body=body).get("_id")

    def update(self, ci_id, body):
        _id = self.get_index_id(ci_id)

        if _id:
            return self.es.index(index=self.index, id=_id, body=body).get("_id")

    def create_or_update(self, ci_id, body):
        try:
            self.update(ci_id, body) or self.create(body)
        except KeyError:
            self.create(body)

    def delete(self, ci_id):
        try:
            _id = self.get_index_id(ci_id)
        except KeyError:
            return

        if _id:
            self.es.delete(index=self.index, id=_id)

    def read(self, query, filter_path=None):
        filter_path = filter_path or []
        if filter_path:
            filter_path.append('hits.total')

        res = self.es.search(index=self.index, body=query, filter_path=filter_path)
        if res['hits'].get('hits'):
            return res['hits']['total']['value'], \
                   [i['_source'] for i in res['hits']['hits']], \
                   res.get("aggregations", {})
        else:
            return 0, [], {}


class Lock(object):
    def __init__(self, name, timeout=10, app=None, need_lock=True):
        self.lock_key = name
        self.need_lock = need_lock
        self.timeout = timeout
        if not app:
            app = current_app
        self.app = app
        try:
            self.redis = redis.Redis(host=self.app.config.get('CACHE_REDIS_HOST'),
                                     port=self.app.config.get('CACHE_REDIS_PORT'),
                                     password=self.app.config.get('CACHE_REDIS_PASSWORD'))
        except:
            self.app.logger.error("cannot connect redis")
            raise Exception("cannot connect redis")

    def lock(self, timeout=None):
        if not timeout:
            timeout = self.timeout
        retry = 0
        while retry < 100:
            timestamp = time.time() + timeout + 1
            _lock = self.redis.setnx(self.lock_key, timestamp)
            if _lock == 1 or (
                    time.time() > float(self.redis.get(self.lock_key) or sys.maxsize) and
                    time.time() > float(self.redis.getset(self.lock_key, timestamp) or sys.maxsize)):
                break
            else:
                retry += 1
                time.sleep(0.6)
        if retry >= 100:
            raise Exception("get lock failed...")

    def release(self):
        if time.time() < float(self.redis.get(self.lock_key)):
            self.redis.delete(self.lock_key)

    def __enter__(self):
        if self.need_lock:
            self.lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.need_lock:
            self.release()


class Redis2Handler(object):
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
                host=config.get("ONEAGENT_REDIS_HOST"),
                port=config.get("ONEAGENT_REDIS_PORT"),
                db=config.get("ONEAGENT_REDIS_DB"),
                password=config.get("ONEAGENT_REDIS_PASSWORD")
            )
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            current_app.logger.warning(str(e))
            current_app.logger.error("init redis connection failed")

    def get(self, key):
        try:
            value = json.loads(self.r.get(key))
        except:
            return

        return value

    def lrange(self, key, start=0, end=-1):
        try:
            value = "".join(map(redis_decode, self.r.lrange(key, start, end) or []))
        except:
            return

        return value

    def lrange2(self, key, start=0, end=-1):
        try:
            return list(map(redis_decode, self.r.lrange(key, start, end) or []))
        except:
            return []

    def llen(self, key):
        try:
            return self.r.llen(key) or 0
        except:
            return 0

    def hget(self, key, field):
        try:
            return self.r.hget(key, field)
        except Exception as e:
            current_app.logger.warning("hget redis failed, %s" % str(e))
            return

    def hset(self, key, field, value):
        try:
            self.r.hset(key, field, value)
        except Exception as e:
            current_app.logger.warning("hset redis failed, %s" % str(e))
            return

    def expire(self, key, timeout):
        try:
            self.r.expire(key, timeout)
        except Exception as e:
            current_app.logger.warning("expire redis failed, %s" % str(e))
            return


def redis_decode(x):
    try:
        return x.decode()
    except Exception as e:
        print(x, e)
        try:
            return x.decode("gb18030")
        except:
            return "decode failed"


class AESCrypto(object):
    BLOCK_SIZE = 16  # Bytes
    pad = lambda s: s + (AESCrypto.BLOCK_SIZE - len(s) % AESCrypto.BLOCK_SIZE) * \
                    chr(AESCrypto.BLOCK_SIZE - len(s) % AESCrypto.BLOCK_SIZE)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    iv = '0102030405060708'

    @staticmethod
    def key():
        key = current_app.config.get("SECRET_KEY")[:16]
        if len(key) < 16:
            key = "{}{}".format(key, (16 - len(key) * "x"))

        return key.encode('utf8')

    @classmethod
    def encrypt(cls, data):
        data = cls.pad(data)
        cipher = AES.new(cls.key(), AES.MODE_CBC, cls.iv.encode('utf8'))

        return base64.b64encode(cipher.encrypt(data.encode('utf8'))).decode('utf8')

    @classmethod
    def decrypt(cls, data):
        encode_bytes = base64.decodebytes(data.encode('utf8'))
        cipher = AES.new(cls.key(), AES.MODE_CBC, cls.iv.encode('utf8'))
        text_decrypted = cipher.decrypt(encode_bytes)

        return cls.unpad(text_decrypted).decode('utf8')
