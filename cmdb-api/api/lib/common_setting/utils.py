# -*- coding:utf-8 -*-
from datetime import datetime


def get_cur_time_str(split_flag='-'):
    f = f"%Y{split_flag}%m{split_flag}%d{split_flag}%H{split_flag}%M{split_flag}%S{split_flag}%f"
    return datetime.now().strftime(f)[:-3]


class BaseEnum(object):
    _ALL_ = set()

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
