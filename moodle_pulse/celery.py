import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moodle_pulse.settings')


celery = Celery('moodle_pulse')

celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/0'
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
