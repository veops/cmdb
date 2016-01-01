# -*- coding:utf-8 -*- 

from extensions import db


class CITypeRelation(db.Model):
    __tablename__ = "ci_type_relations"

    ctr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer,
                          db.ForeignKey("ci_types.type_id"),
                          primary_key=True)
    parent = db.relationship(
        "CIType", primaryjoin="CIType.type_id==CITypeRelation.parent_id")
    child_id = db.Column(db.Integer,
                         db.ForeignKey("ci_types.type_id"),
                         primary_key=True)
    child = db.relationship(
        "CIType", primaryjoin="CIType.type_id==CITypeRelation.child_id")
    relation_type = db.Column(
        db.String(7),
        db.Enum("contain", "connect", "deploy", "install",
                name="relation_type"),
        default="contain")

    __table_args__ = (db.UniqueConstraint("parent_id", "child_id",
                                          name="parent_child_uniq"), )