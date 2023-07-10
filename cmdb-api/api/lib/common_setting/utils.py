# -*- coding:utf-8 -*-
from datetime import datetime

import pandas as pd
from sqlalchemy import text

from api.extensions import db


def get_df_from_read_sql(query, to_dict=False):
    bind = query.session.bind
    query = query.statement.compile(dialect=bind.dialect if bind else None,
                                    compile_kwargs={"literal_binds": True}).string
    a = db.engine
    df = pd.read_sql(sql=text(query), con=a.connect())

    if to_dict:
        return df.to_dict('records')
    return df


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
