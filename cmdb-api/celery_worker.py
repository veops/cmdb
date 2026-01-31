# -*- coding:utf-8 -*-

from api.app import create_app
from api.extensions import celery
from celery.schedules import crontab

# celery -A celery_worker.celery worker -l DEBUG -E -Q xxxx

app = create_app()
app.app_context().push()

# Beat schedule configuration
celery.conf.beat_schedule = {
    'cmdb-counter-main': {
        'task': 'cmdb.counter_main',
        'schedule': crontab(minute='*'),
    },
    'cmdb-counter-adc': {
        'task': 'cmdb.counter_adc',
        'schedule': crontab(minute='*/5'),
    },
    'cmdb-counter-daily': {
        'task': 'cmdb.counter_daily',
        'schedule': crontab(hour=0, minute=0),
    },
}
