import requests
from moodle_pulse.celery import celery

from app.models import monitored_instance


celery.conf.beat_schedule = {
    'collect': {
        'task': 'tasks.collect',
        'schedule': 30.0,
        'args': ()
    }
}

@celery.task(name='tasks.collect')
def collect():
    servers = monitored_instance.objects.all().filter(active=True)
    for server in servers:
        heartbeat = requests.get(server.base_url)
        print(heartbeat)