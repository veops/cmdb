# -*- coding:utf-8 -*-

from api.app import create_app
from api.extensions import celery

# celery worker -A celery_worker.celery -l DEBUG -E -Q <queue_name> --concurrency=1
print(celery)

app = create_app()
app.app_context().push()
