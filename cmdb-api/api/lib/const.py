# -*- coding:utf-8 -*-

from api.lib.utils import BaseEnum


class PermEnum(BaseEnum):
    ADD = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    EXECUTE = "execute"
    GRANT = "grant"
    ADMIN = "admin"


class RoleEnum(BaseEnum):
    ADMIN = "OneOPS_Application_Admin"
