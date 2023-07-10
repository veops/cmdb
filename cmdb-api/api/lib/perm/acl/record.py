# -*- coding:utf-8 -*-

from api.models.acl import OperationRecord


class OperateRecordCRUD(object):
    @staticmethod
    def search(page, page_size, **kwargs):
        query = OperationRecord.get_by(only_query=True)
        for k, v in kwargs.items():
            if hasattr(OperationRecord, k) and v:
                query = query.filter(getattr(OperationRecord, k) == v)

        numfound = query.count()
        res = query.offset((page - 1) * page_size).limit(page_size)

        return numfound, res

    @staticmethod
    def add(app, rolename, operate, obj):
        OperationRecord.create(app=app, rolename=rolename, operate=operate, obj=obj)
