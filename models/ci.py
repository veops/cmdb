# -*- coding:utf-8 -*- 

import datetime

from extensions import db


class CI(db.Model):
    __tablename__ = "cis"

    ci_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(32), nullable=False)
    type_id = db.Column(db.Integer,
                        db.ForeignKey("ci_types.type_id"),
                        nullable=False)
    ci_type = db.relationship("CIType", backref="cis")
    status = db.Column(db.Enum("review", "validate", name="status"))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    heartbeat = db.Column(db.DateTime, default=datetime.datetime.now())
