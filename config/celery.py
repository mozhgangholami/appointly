import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = 'redis://redis:6379/0'

app.conf.beat_schedule = {
    'send_reminders_daily': {
        'task': 'booking.tasks.send_daily_reminders',
        'schedule': crontab(hour=10, minute=0),  # هر روز ساعت 10 صبح
    },
}


@app.task(bind=True)


def debug_task(self):
    print(f'Request: {self.request!r}')



