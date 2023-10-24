import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'replicator.settings')

app = Celery('replicator')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
