# -*- coding:utf-8 -*-


def row2dict(row):
    d = dict()
    for c in row.__table__.columns:
        if not isinstance(getattr(row, c.name),
                          (basestring, long, int, float, list, tuple, dict)) \
                and getattr(row, c.name):
            d[c.name] = getattr(row, c.name).strftime("%Y-%m-%d %H:%M:%S")
        else:
            d[c.name] = getattr(row, c.name)
    return d