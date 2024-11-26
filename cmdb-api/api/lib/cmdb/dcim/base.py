# -*- coding:utf-8 -*-

from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import ExistPolicy


class DCIMBase(object):
    def __init__(self):
        self.type_id = None

    @staticmethod
    def add_relation(parent_id, child_id):
        if not parent_id or not child_id:
            return

        CIRelationManager().add(parent_id, child_id, valid=False, apply_async=False)

    def add(self, parent_id, **kwargs):
        ci_id = CIManager().add(self.type_id, exist_policy=ExistPolicy.REJECT, **kwargs)

        if parent_id:
            self.add_relation(parent_id, ci_id)

        return ci_id

    @classmethod
    def update(cls, _id, **kwargs):
        CIManager().update(_id, **kwargs)

    @classmethod
    def delete(cls, _id):
        CIManager().delete(_id)
