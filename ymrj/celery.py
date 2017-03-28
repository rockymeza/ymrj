import os

from celery import Celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ymrj.settings')


class InstrumentedCelery(Celery):
    def on_configure(self):
        client = raven.Client(os.environ.get('SENTRY_DSN'))
        register_logger_signal(client)
        register_signal(client)


app = InstrumentedCelery('ymrj')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
