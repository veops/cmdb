# -*- coding:utf-8 -*-


import datetime

from api.extensions import db
from api.lib.database import Model


# template

class RelationType(Model):
    __tablename__ = "c_relation_types"

    name = db.Column(db.String(16), index=True)


class CITypeGroup(Model):
    __tablename__ = "c_ci_type_groups"

    name = db.Column(db.String(32))


class CITypeGroupItem(Model):
    __tablename__ = "c_ci_type_group_items"

    group_id = db.Column(db.Integer, db.ForeignKey("c_ci_type_groups.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    order = db.Column(db.SmallInteger, default=0)


class CIType(Model):
    __tablename__ = "c_ci_types"

    name = db.Column(db.String(32))
    alias = db.Column(db.String(32))
    unique_id = db.Column(db.Integer, db.ForeignKey("c_attributes.id"), nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    is_attached = db.Column(db.Boolean, default=False, nullable=False)
    icon_url = db.Column(db.String(256))
    order = db.Column(db.SmallInteger, default=0, nullable=False)

    unique_key = db.relationship("Attribute", backref="c_ci_types.unique_id")


class CITypeRelation(Model):
    __tablename__ = "c_ci_type_relations"

    parent_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    relation_type_id = db.Column(db.Integer, db.ForeignKey("c_relation_types.id"), nullable=False)

    parent = db.relationship("CIType", primaryjoin="CIType.id==CITypeRelation.parent_id")
    child = db.relationship("CIType", primaryjoin="CIType.id==CITypeRelation.child_id")
    relation_type = db.relationship("RelationType", backref="c_ci_type_relations.relation_type_id")


class Attribute(Model):
    __tablename__ = "c_attributes"

    INT = "0"
    FLOAT = "1"
    TEXT = "2"
    DATETIME = "3"
    DATE = "4"
    TIME = "5"

    name = db.Column(db.String(32), nullable=False)
    alias = db.Column(db.String(32), nullable=False)
    value_type = db.Column(db.Enum(INT, FLOAT, TEXT, DATETIME, DATE, TIME), default=TEXT, nullable=False)

    is_choice = db.Column(db.Boolean, default=False)
    is_list = db.Column(db.Boolean, default=False)
    is_unique = db.Column(db.Boolean, default=False)
    is_index = db.Column(db.Boolean, default=False)
    is_link = db.Column(db.Boolean, default=False)
    is_password = db.Column(db.Boolean, default=False)
    is_sortable = db.Column(db.Boolean, default=False)


class CITypeAttribute(Model):
    __tablename__ = "c_ci_type_attributes"

    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey("c_attributes.id"), nullable=False)
    order = db.Column(db.Integer, default=0)
    is_required = db.Column(db.Boolean, default=False)
    default_show = db.Column(db.Boolean, default=True)

    attr = db.relationship("Attribute", backref="c_ci_type_attributes.attr_id")


class CITypeAttributeGroup(Model):
    __tablename__ = "c_ci_type_attribute_groups"

    name = db.Column(db.String(64))
    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    order = db.Column(db.SmallInteger, default=0)


class CITypeAttributeGroupItem(Model):
    __tablename__ = "c_ci_type_attribute_group_items"

    group_id = db.Column(db.Integer, db.ForeignKey("c_ci_type_attribute_groups.id"), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey("c_attributes.id"), nullable=False)
    order = db.Column(db.SmallInteger, default=0)


# instance

class CI(Model):
    __tablename__ = "c_cis"

    REVIEW = "0"
    VALIDATE = "1"

    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    status = db.Column(db.Enum(REVIEW, VALIDATE, name="status"))
    heartbeat = db.Column(db.DateTime, default=lambda: datetime.datetime.now())

    ci_type = db.relationship("CIType", backref="c_cis.type_id")


class CIRelation(Model):
    __tablename__ = "c_ci_relations"

    first_ci_id = db.Column(db.Integer, db.ForeignKey("c_cis.id"), nullable=False)
    second_ci_id = db.Column(db.Integer, db.ForeignKey("c_cis.id"), nullable=False)
    relation_type_id = db.Column(db.Integer, db.ForeignKey("c_relation_types.id"), nullable=False)
    more = db.Column(db.Integer, db.ForeignKey("c_cis.id"))

    first_ci = db.relationship("CI", primaryjoin="CI.id==CIRelation.first_ci_id")
    second_ci = db.relationship("CI", primaryjoin="CI.id==CIRelation.second_ci_id")
    relation_type = db.relationship("RelationType", backref="c_ci_relations.relation_type_id")


class IntegerChoice(Model):
    __tablename__ = 'c_choice_integers'

    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    attr = db.relationship("Attribute", backref="c_choice_integers.attr_id")


class FloatChoice(Model):
    __tablename__ = 'c_choice_floats'

    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    attr = db.relationship("Attribute", backref="c_choice_floats.attr_id")


class TextChoice(Model):
    __tablename__ = 'c_choice_texts'

    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Text, nullable=False)

    attr = db.relationship("Attribute", backref="c_choice_texts.attr_id")


class CIIndexValueInteger(Model):
    __tablename__ = "c_value_index_integers"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    ci = db.relationship("CI", backref="c_value_index_integers.ci_id")
    attr = db.relationship("Attribute", backref="c_value_index_integers.attr_id")

    __table_args__ = (db.Index("integer_attr_value_index", "attr_id", "value"),)


class CIIndexValueFloat(Model):
    __tablename__ = "c_value_index_floats"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    ci = db.relationship("CI", backref="c_value_index_floats.ci_id")
    attr = db.relationship("Attribute", backref="c_value_index_floats.attr_id")

    __table_args__ = (db.Index("float_attr_value_index", "attr_id", "value"),)


class CIIndexValueText(Model):
    __tablename__ = "c_value_index_texts"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.String(128), nullable=False)

    ci = db.relationship("CI", backref="c_value_index_texts.ci_id")
    attr = db.relationship("Attribute", backref="c_value_index_texts.attr_id")

    __table_args__ = (db.Index("text_attr_value_index", "attr_id", "value"),)


class CIIndexValueDateTime(Model):
    __tablename__ = "c_value_index_datetime"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.DateTime, nullable=False)

    ci = db.relationship("CI", backref="c_value_index_datetime.ci_id")
    attr = db.relationship("Attribute", backref="c_value_index_datetime.attr_id")

    __table_args__ = (db.Index("datetime_attr_value_index", "attr_id", "value"),)


class CIValueInteger(Model):
    __tablename__ = "c_value_integers"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    ci = db.relationship("CI", backref="c_value_integers.ci_id")
    attr = db.relationship("Attribute", backref="c_value_integers.attr_id")


class CIValueFloat(Model):
    __tablename__ = "c_value_floats"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    ci = db.relationship("CI", backref="c_value_floats.ci_id")
    attr = db.relationship("Attribute", backref="c_value_floats.attr_id")


class CIValueText(Model):
    __tablename__ = "c_value_texts"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.Text, nullable=False)

    ci = db.relationship("CI", backref="c_value_texts.ci_id")
    attr = db.relationship("Attribute", backref="c_value_texts.attr_id")


class CIValueDateTime(Model):
    __tablename__ = "c_value_datetime"

    ci_id = db.Column(db.Integer, db.ForeignKey('c_cis.id'), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey('c_attributes.id'), nullable=False)
    value = db.Column(db.DateTime, nullable=False)

    ci = db.relationship("CI", backref="c_value_datetime.ci_id")
    attr = db.relationship("Attribute", backref="c_value_datetime.attr_id")


# history
class OperationRecord(Model):
    __tablename__ = "c_records"

    uid = db.Column(db.Integer, index=True, nullable=False)
    origin = db.Column(db.String(32))
    ticket_id = db.Column(db.String(32))
    reason = db.Column(db.Text)


class AttributeHistory(Model):
    __tablename__ = "c_attribute_histories"

    ADD = "0"
    DELETE = "1"
    UPDATE = "2"

    operate_type = db.Column(db.Enum(ADD, DELETE, UPDATE, name="operate_type"))
    record_id = db.Column(db.Integer, db.ForeignKey("c_records.id"), nullable=False)
    ci_id = db.Column(db.Integer, index=True, nullable=False)
    attr_id = db.Column(db.Integer, index=True)
    old = db.Column(db.Text)
    new = db.Column(db.Text)


class CIRelationHistory(Model):
    __tablename__ = "c_relation_histories"

    ADD = "0"
    DELETE = "1"

    operate_type = db.Column(db.Enum(ADD, DELETE, name="operate_type"))
    record_id = db.Column(db.Integer, db.ForeignKey("c_records.id"), nullable=False)
    first_ci_id = db.Column(db.Integer)
    second_ci_id = db.Column(db.Integer)
    relation_type_id = db.Column(db.Integer, db.ForeignKey("c_relation_types.id"))
    relation_id = db.Column(db.Integer, nullable=False)


# preference
class PreferenceShowAttributes(Model):
    __tablename__ = "c_preference_show_attributes"

    uid = db.Column(db.Integer, index=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey("c_attributes.id"))
    order = db.Column(db.SmallInteger, default=0)

    ci_type = db.relationship("CIType", backref="c_preference_show_attributes.type_id")
    attr = db.relationship("Attribute", backref="c_preference_show_attributes.attr_id")


class PreferenceTreeView(Model):
    __tablename__ = "c_preference_tree_views"

    uid = db.Column(db.Integer, index=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    levels = db.Column(db.Text)  # TODO: JSON


class PreferenceRelationView(Model):
    __tablename__ = "c_preference_relation_views"

    name = db.Column(db.String(8), index=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("c_ci_types.id"), nullable=False)
