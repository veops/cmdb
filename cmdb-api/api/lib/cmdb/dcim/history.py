from flask_login import current_user

from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.mixin import DBMixin
from api.models.cmdb import DCIMOperationHistory


class OperateHistoryManager(DBMixin):
    cls = DCIMOperationHistory

    @classmethod
    def search(cls, page, page_size, fl=None, only_query=False, reverse=False, count_query=False,
               last_size=None, **kwargs):
        numfound, result = super(OperateHistoryManager, cls).search(page, page_size, fl, only_query, reverse,
                                                                    count_query, last_size, **kwargs)

        ci_ids = [i['ci_id'] for i in result]
        id2ci = {i['_id']: i for i in (CIManager.get_cis_by_ids(ci_ids) or []) if i}
        type2show_key = dict()
        for i in id2ci.values():
            if i.get('_type') not in type2show_key:
                ci_type = CITypeCache.get(i.get('_type'))
                if ci_type:
                    show_key = AttributeCache.get(ci_type.show_id or ci_type.unique_id)
                    type2show_key[i['_type']] = show_key and show_key.name

        return numfound, result, id2ci, type2show_key

    def _can_add(self, **kwargs):
        kwargs['uid'] = current_user.uid

        return kwargs

    def _can_update(self, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        pass
