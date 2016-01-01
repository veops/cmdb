# -*- coding:utf-8 -*- 

from extensions import db
from extensions import cache


class CIType(db.Model):
    __tablename__ = "ci_types"

    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(32))
    type_alias = db.Column(db.String(32))
    uniq_id = db.Column(db.Integer,
                        db.ForeignKey("ci_attributes.attr_id"),
                        nullable=False)
    uniq_key = db.relationship("CIAttribute", backref="ci_types")
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    is_attached = db.Column(db.Boolean, default=False, nullable=False)
    icon_url = db.Column(db.String(256))
    order = db.Column(db.SmallInteger, default=0, nullable=False)


class CITypeAttribute(db.Model):
    __tablename__ = "type_attributes"

    type_id = db.Column(db.Integer,
                        db.ForeignKey("ci_types.type_id"),
                        primary_key=True)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey("ci_attributes.attr_id"),
                        primary_key=True)
    is_required = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint("type_id", "attr_id",
                                          name="type_attr_uniq"), )


class CITypeCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get("CIType::ID::%s" % key) or \
            cache.get("CIType::Name::%s" % key)
        if ct is None:
            ct = db.session.query(CIType).filter(
                CIType.type_name == key).first() or \
                db.session.query(CIType).filter(CIType.type_id == key).first()
            if ct is not None:
                CITypeCache.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set("CIType::Name::%s" % ct.type_name, ct)
        cache.set("CIType::ID::%d" % ct.type_id, ct)

    @classmethod
    def clean(cls, key):
        ct = CITypeCache.get(key)
        if ct is not None:
            cache.delete("CIType::Name::%s" % ct.type_name)
            cache.delete("CIType::ID::%s" % ct.type_id)


class CITypeSpecCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        ct = cache.get("CITypeSPEC::ID::%d" % key)
        if ct is None:
            ct = db.session.query(CIType).filter(CIType.type_id == key).first()
            if ct is not None:
                CITypeSpecCache.set(ct)
        return ct

    @classmethod
    def set(cls, ct):
        cache.set("CITypeSPEC::ID::%d" % ct.type_id, ct)

    @classmethod
    def clean(cls, key):
        ct = CITypeCache.get(key)
        if ct is not None:
            cache.delete("CITypeSPEC::ID::%d" % ct.type_id)


class CITypeAttributeCache(object):
    """
    key is type_id or type_name
    """

    @classmethod
    def get(cls, key):
        if key is None:
            return
        if isinstance(key, basestring) and isinstance(key, unicode):
            key = unicode(key, 'utf8')
        citypes = cache.get("CITypeAttribute::Name::%s" % key) or \
            cache.get("CITypeAttribute::ID::%s" % key)
        if not citypes:
            citypes = db.session.query(CITypeAttribute).filter(
                CITypeAttribute.type_id == key).all()
            if citypes is None:
                ci_type = db.session.query(CIType).filter(
                    CIType.type_name == key).first()
                if ci_type is not None:
                    citypes = db.session.query(CITypeAttribute).filter_by(
                        type_id=ci_type.type_id).all()
            if citypes is not None:
                CITypeAttributeCache.set(key, citypes)
        return citypes

    @classmethod
    def set(cls, key, values):
        citype = CITypeCache.get(key)
        if citype is not None:
            cache.set("CITypeAttribute::ID::%s" % citype.type_id, values)
            cache.set("CITypeAttribute::Name::%s" % citype.type_name, values)

    @classmethod
    def clean(cls, key):
        citype = CITypeCache.get(key)
        attrs = CITypeAttributeCache.get(key)
        if attrs is not None and citype:
            cache.delete("CITypeAttribute::ID::%s" % citype.type_id)
            cache.delete("CITypeAttribute::Name::%s" % citype.type_name)