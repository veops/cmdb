# -*- coding:utf-8 -*-

from api.app import create_app
from api.extensions import celery

# celery worker -A celery_worker.celery -l DEBUG -E -Q xxxx

app = create_app()
app.app_context().push()
