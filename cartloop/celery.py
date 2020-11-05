import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartloop.settings')

app = Celery('cartloop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "every-hour": {
        "task": "send_emails",
        "schedule": crontab(minute=0),
        # "schedule": crontab(), # For test run every minute

    },
}

app.autodiscover_tasks()