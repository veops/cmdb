# -*- coding:utf-8 -*-

from api.lib.utils import BaseEnum

ACL_QUEUE = "acl_async"


class OperateType(BaseEnum):
    LOGIN = "0"
    READ = "1"
    UPDATE = "2"
    CREATE = "3"
    DELETE = "4"
