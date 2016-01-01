# -*- coding:utf-8 -*- 


from extensions import db
from sqlalchemy import Index


class CIIndexValueInteger(db.Model):
    __tablename__ = "index_integers"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="index_integers")
    attr = db.relationship("CIAttribute", backref="index_integers")
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (Index("attr_value_index", "attr_id", "value"), )


class CIIndexValueFloat(db.Model):
    __tablename__ = "index_floats"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="index_floats")
    attr = db.relationship("CIAttribute", backref="index_floats")
    value = db.Column(db.Float, nullable=False)

    __table_args__ = (Index("attr_value_index", "attr_id", "value"), )


class CIIndexValueText(db.Model):
    __tablename__ = "index_texts"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="index_texts")
    attr = db.relationship("CIAttribute", backref="index_texts")
    value = db.Column(db.String(128), nullable=False)

    __table_args__ = (Index("attr_value_index", "attr_id", "value"), )


class CIIndexValueDateTime(db.Model):
    __tablename__ = "index_datetime"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="index_datetime")
    attr = db.relationship("CIAttribute", backref="index_datetime")
    value = db.Column(db.DateTime, nullable=False)

    __table_args__ = (Index("attr_value_index", "attr_id", "value"), )


class CIValueInteger(db.Model):
    __tablename__ = "integers"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="integers")
    attr = db.relationship("CIAttribute", backref="integers")
    value = db.Column(db.Integer, nullable=False)


class CIValueFloat(db.Model):
    __tablename__ = "floats"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="floats")
    attr = db.relationship("CIAttribute", backref="floats")
    value = db.Column(db.Float, nullable=False)


class CIValueText(db.Model):
    __tablename__ = "texts"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="texts")
    attr = db.relationship("CIAttribute", backref="texts")
    value = db.Column(db.Text, nullable=False)


class CIValueDateTime(db.Model):
    __tablename__ = "datetime"

    value_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_id = db.Column(db.Integer, db.ForeignKey('cis.ci_id'), nullable=False)
    attr_id = db.Column(db.Integer,
                        db.ForeignKey('ci_attributes.attr_id'),
                        nullable=False)
    ci = db.relationship("CI", backref="datetime")
    attr = db.relationship("CIAttribute", backref="datetime")
    value = db.Column(db.DateTime, nullable=False)
