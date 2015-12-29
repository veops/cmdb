# -*- coding:utf-8 -*- 


import datetime

from flask import current_app

from extensions import celery
from extensions import db
from models.statis import UrlRecord


@celery.task(name="statis.url_record", queue="statis_async")
def url_record(url, method, remote_addr, response_time, status_code, source):
    current_app.logger.info("%s add 1" % url)
    now = datetime.datetime.now()
    u = UrlRecord(url=url, response_time=response_time, is_ok=1,
                  source="default", hits=1, method=method, created_at=now,
                  remote_addr=remote_addr)
    db.session.add(u)
    db.session.commit()