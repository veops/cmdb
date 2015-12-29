# -*- coding:utf-8 -*- 


def convert_to_list(v):
    if isinstance(v, list):
        return v
    if isinstance(v, tuple):
        return list(v)
    return [v, ]
