# -*- coding:utf-8 -*-

import datetime

import six

from api.extensions import db
from api.lib.exception import CommitException


class FormatMixin(object):
    def to_dict(self):
        res = dict()
        for k in getattr(self, "__table__").columns:
            if not isinstance(getattr(self, k.name), datetime.datetime):
                res[k.name] = getattr(self, k.name)
            else:
                res[k.name] = getattr(self, k.name).strftime('%Y-%m-%d %H:%M:%S')

        return res

    @classmethod
    def get_columns(cls):
        return {k.name: 1 for k in getattr(cls, "__mapper__").c.values()}


class CRUDMixin(FormatMixin):
    @classmethod
    def create(cls, flush=False, **kwargs):
        return cls(**kwargs).save(flush=flush)

    def update(self, flush=False, **kwargs):
        kwargs.pop("id", None)
        for attr, value in six.iteritems(kwargs):
            if value is not None:
                setattr(self, attr, value)
        if flush:
            return self.save(flush=flush)
        return self.save()

    def save(self, commit=True, flush=False):
        db.session.add(self)
        try:
            if flush:
                db.session.flush()
            elif commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

        return self

    def delete(self, flush=False):
        db.session.delete(self)
        try:
            if flush:
                return db.session.flush()
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

    def soft_delete(self, flush=False):
        setattr(self, "deleted", True)
        setattr(self, "deleted_at", datetime.datetime.now())
        self.save(flush=flush)

    @classmethod
    def get_by_id(cls, _id):
        if any((isinstance(_id, six.string_types) and _id.isdigit(),
                isinstance(_id, (six.integer_types, float))), ):
            return getattr(cls, "query").get(int(_id)) or None

    @classmethod
    def get_by(cls, first=False, to_dict=True, fl=None, exclude=None, deleted=False, use_master=False, **kwargs):
        db_session = db.session if not use_master else db.session().using_bind("master")
        fl = fl.strip().split(",") if fl and isinstance(fl, six.string_types) else (fl or [])
        exclude = exclude.strip().split(",") if exclude and isinstance(exclude, six.string_types) else (exclude or [])

        keys = cls.get_columns()
        fl = [k for k in fl if k in keys]
        fl = [k for k in keys if k not in exclude and not k.isupper()] if exclude else fl
        fl = list(filter(lambda x: "." not in x, fl))

        if hasattr(cls, "deleted") and deleted is not None:
            kwargs["deleted"] = deleted

        if fl:
            query = db_session.query(*[getattr(cls, k) for k in fl])
            query = query.filter_by(**kwargs)
            result = [{k: getattr(i, k) for k in fl} for i in query]
        else:
            result = [i.to_dict() if to_dict else i for i in getattr(cls, 'query').filter_by(**kwargs)]

        return result[0] if first and result else (None if first else result)

    @classmethod
    def get_by_like(cls, to_dict=True, **kwargs):
        query = db.session.query(cls)
        for k, v in kwargs.items():
            query = query.filter(getattr(cls, k).ilike('%{0}%'.format(v)))
        return [i.to_dict() if to_dict else i for i in query]


class SoftDeleteMixin(object):
    deleted_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, index=True, default=False)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.datetime.now())


class SurrogatePK(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Model(SoftDeleteMixin, TimestampMixin, CRUDMixin, db.Model, SurrogatePK):
    __abstract__ = True


class CRUDModel(db.Model, CRUDMixin):
    __abstract__ = True
