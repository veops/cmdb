# -*- coding:utf-8 -*-

__all__ = ['ci', 'ci_relation', 'SearchError']


class SearchError(Exception):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return self.v
