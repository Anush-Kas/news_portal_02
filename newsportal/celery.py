import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_digest': {
        'task': 'posts.tasks.weekly_posts',
        'schedule': crontab(day_of_week='mon', hour=8),
        'args': [],
    },
}
