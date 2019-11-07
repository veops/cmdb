# -*- coding:utf-8 -*-

from flask import current_app

from api.extensions import celery


@celery.task(queue="ticket_web")
def test_task():
    current_app.logger.info("test task.............................")
