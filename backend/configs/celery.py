import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')


app = Celery('AutoRia-Clone')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-premium-listing-prices': {
        'task': 'core.tasks.avg_price_task',
        'schedule': crontab(minute=0, hour=4)
    },
    'update_exchange_rates': {
        'task': 'core.tasks.exchange.update_exchange_rates',
        'schedule': crontab(minute=0, hour=4)
    },
}
