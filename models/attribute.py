# -*- coding:utf-8 -*- 

from extensions import db, cache


class CIAttribute(db.Model):
    __tablename__ = "ci_attributes"

    attr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attr_name = db.Column(db.String(32), nullable=False, unique=True)
    attr_alias = db.Column(db.String(32), nullable=False, unique=True)
    value_type = db.Column(
        db.String(8),
        db.Enum("int", "float", "text", "datetime", name='value_type'),
        default="text",
        nullable=False)
    is_choice = db.Column(db.Boolean, default=False)
    is_multivalue = db.Column(db.Boolean, default=False)
    is_uniq = db.Column(db.Boolean, default=False)
    is_index = db.Column(db.Boolean, default=False)


class IntegerChoice(db.Model):
    __tablename__ = 'choice_integers'

    choice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    attr = db.relationship("CIAttribute", backref="choice_integers")
    value = db.Column(db.Integer, nullable=False)


class FloatChoice(db.Model):
    __tablename__ = 'choice_floats'

    choice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    attr = db.relationship("CIAttribute", backref="choice_floats")
    value = db.Column(db.Float, nullable=False)


class TextChoice(db.Model):
    __tablename__ = 'choice_texts'

    choice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    attr = db.relationship("CIAttribute", backref="choice_texts")
    value = db.Column(db.Text, nullable=False)


class CIAttributeCache(object):
    @classmethod
    def get(cls, key):
        if key is None:
            return
        attr = cache.get('Field::Name::%s' % key) or \
               cache.get('Field::ID::%s' % key) or \
               cache.get('Field::Alias::%s' % key)
        if attr is None:
            attr = db.session.query(CIAttribute).filter_by(
                attr_name=key).first() or \
                   db.session.query(CIAttribute).filter(
                       CIAttribute.attr_id == key).first() or \
                   db.session.query(CIAttribute).filter(
                       CIAttribute.attr_alias == key).first()
            db.session.close()
            if attr is not None:
                CIAttributeCache.set(attr)
        return attr

    @classmethod
    def set(cls, attr):
        cache.set('Field::ID::%s' % attr.attr_id, attr)
        cache.set('Field::Name::%s' % attr.attr_name, attr)
        cache.set('Field::Alias::%s' % attr.attr_alias, attr)

    @classmethod
    def clean(cls, attr):
        if cache.get('Field::ID::%s' % attr.attr_id):
            cache.delete('Field::ID::%s' % attr.attr_id)
            cache.delete('Field::Name::%s' % attr.attr_name)
            cache.delete('Field::Alias::%s' % attr.attr_alias)