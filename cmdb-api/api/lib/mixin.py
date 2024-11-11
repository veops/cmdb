# -*- coding:utf-8 -*-


from flask import current_app
from sqlalchemy import func

from api.extensions import db
from api.lib.utils import get_page
from api.lib.utils import get_page_size


class DBMixin(object):
    cls = None

    @classmethod
    def search(cls, page, page_size, fl=None, only_query=False, reverse=False, count_query=False,
               last_size=None, **kwargs):
        page = get_page(page)
        page_size = get_page_size(page_size)
        if fl is None:
            query = db.session.query(cls.cls)
        else:
            query = db.session.query(*[getattr(cls.cls, i) for i in fl])

        _query = None
        if count_query:
            _query = db.session.query(func.count(cls.cls.id))

        if hasattr(cls.cls, 'deleted'):
            query = query.filter(cls.cls.deleted.is_(False))
            if _query:
                _query = _query.filter(cls.cls.deleted.is_(False))

        for k in kwargs:
            if hasattr(cls.cls, k):
                if isinstance(kwargs[k], list):
                    query = query.filter(getattr(cls.cls, k).in_(kwargs[k]))
                    if count_query:
                        _query = _query.filter(getattr(cls.cls, k).in_(kwargs[k]))
                else:
                    if "*" in str(kwargs[k]):
                        query = query.filter(getattr(cls.cls, k).ilike(kwargs[k].replace('*', '%')))
                        if count_query:
                            _query = _query.filter(getattr(cls.cls, k).ilike(kwargs[k].replace('*', '%')))
                    else:
                        query = query.filter(getattr(cls.cls, k) == kwargs[k])
                        if count_query:
                            _query = _query.filter(getattr(cls.cls, k) == kwargs[k])

        if reverse in current_app.config.get('BOOL_TRUE'):
            query = query.order_by(cls.cls.id.desc())

        if only_query and not count_query:
            return query
        elif only_query:
            return _query, query

        numfound = query.count()
        if not last_size:
            return numfound, [i.to_dict() if fl is None else getattr(i, '_asdict')()
                              for i in query.offset((page - 1) * page_size).limit(page_size)]
        else:
            offset = numfound - last_size
            if offset < 0:
                offset = 0
            return numfound, [i.to_dict() if fl is None else getattr(i, '_asdict')()
                              for i in query.offset(offset).limit(last_size)]

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
