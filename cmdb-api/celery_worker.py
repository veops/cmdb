# -*- coding:utf-8 -*-

from api.app import create_app
from api.extensions import celery

# celery -A celery_worker.celery worker -l DEBUG -E -Q xxxx

app = create_app()
app.app_context().push()

# Load beat schedules from all modules
from api.tasks.cmdb import CMDB_BEAT_SCHEDULE

celery.conf.beat_schedule = celery.conf.get('beat_schedule', {})
celery.conf.beat_schedule.update(CMDB_BEAT_SCHEDULE)
