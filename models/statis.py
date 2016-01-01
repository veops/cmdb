# -*- coding:utf-8 -*- 


import datetime

from extensions import db


class UrlRecord(db.Model):

    url_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    url = db.Column(db.String(64), nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    is_ok = db.Column(db.Boolean, default=True)
    source = db.Column(db.String(32))
    remote_addr = db.Column(db.String(20))
    hits = db.Column(db.Integer)
    method = db.Column(db.String(5), default="GET")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())