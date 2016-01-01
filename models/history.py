# -*- coding:utf-8 -*- 


import datetime

from extensions import db


class OperationRecord(db.Model):
    __tablename__ = "records"

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.now())
    origin = db.Column(db.String(32))
    ticket_id = db.Column(db.String(32))
    reason = db.Column(db.Text)


class CIAttributeHistory(db.Model):
    __tablename__ = "histories"

    h_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operate_type = db.Column(db.String(6), db.Enum("add", "delete", "update",
                                                   name="operate_type"))
    record_id = db.Column(db.Integer,
                          db.ForeignKey("records.record_id"),
                          nullable=False)
    ci_id = db.Column(db.Integer, nullable=False)
    attr_id = db.Column(db.Integer, nullable=False)
    old = db.Column(db.Text)
    new = db.Column(db.Text)


class CIRelationHistory(db.Model):
    __tablename__ = "relation_histories"

    rh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operate_type = db.Column(db.String(6),
                             db.Enum("add", "delete", name="operate_type"))
    record_id = db.Column(db.Integer,
                          db.ForeignKey("records.record_id"),
                          nullable=False)
    first_ci_id = db.Column(db.Integer)
    second_ci_id = db.Column(db.Integer)
    relation_type = db.Column(
        db.String(8), db.Enum("connect", "deploy", "install", "contain",
                              name="relation_type"))
    relation = db.Column(db.Integer, nullable=False)
