# -*- coding:utf-8 -*-


from flask import abort
from sqlalchemy import func

from api.extensions import db
from api.lib.utils import get_page
from api.lib.utils import get_page_size


class DBMixin(object):
    cls = None

    @classmethod
    def search(cls, page, page_size, fl=None, only_query=False, reverse=False, count_query=False, **kwargs):
        page = get_page(page)
        page_size = get_page_size(page_size)
        if fl is None:
            query = db.session.query(cls.cls).filter(cls.cls.deleted.is_(False))
        else:
            query = db.session.query(*[getattr(cls.cls, i) for i in fl]).filter(cls.cls.deleted.is_(False))

        _query = None
        if count_query:
            _query = db.session.query(func.count(cls.cls.id)).filter(cls.cls.deleted.is_(False))

        for k in kwargs:
            if hasattr(cls.cls, k):
                query = query.filter(getattr(cls.cls, k) == kwargs[k])
                if count_query:
                    _query = _query.filter(getattr(cls.cls, k) == kwargs[k])

        if reverse:
            query = query.order_by(cls.cls.id.desc())

        if only_query and not count_query:
            return query
        elif only_query:
            return _query, query

        numfound = query.count()
        return numfound, [i.to_dict() if fl is None else getattr(i, '_asdict')()
                          for i in query.offset((page - 1) * page_size).limit(page_size)]

    def _must_be_required(self, _id):
        existed = self.cls.get_by_id(_id)
        existed or abort(404, "Factor [{}] does not exist".format(_id))

        return existed

    def _can_add(self, **kwargs):
        raise NotImplementedError

    def _after_add(self, obj, **kwargs):
        pass

    def _can_update(self, **kwargs):
        raise NotImplementedError

    def _after_update(self, obj, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        raise NotImplementedError

    def _after_delete(self, obj):
        pass

    def add(self, **kwargs):
        kwargs = self._can_add(**kwargs) or kwargs

        obj = self.cls.create(**kwargs)

        kwargs['_id'] = obj.id if hasattr(obj, 'id') else None
        self._after_add(obj, **kwargs)

        return obj

    def update(self, _id, **kwargs):
        inst = self._can_update(_id=_id, **kwargs)

        obj = inst.update(_id=_id, **kwargs)

        self._after_update(obj, **kwargs)

        return obj

    def delete(self, _id):
        inst = self._can_delete(_id=_id)

        inst.soft_delete()

        self._after_delete(inst)

        return inst
