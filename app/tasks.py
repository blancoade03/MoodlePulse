import requests
import time
from django.db import transaction
from datetime import datetime, timedelta
from typing import Dict, Optional

from moodle_pulse import settings
from moodle_pulse.celery import celery

from app.models import monitored_instance, moodle_heartbeat
from app.serializers import moodle_hearbeatSerializer
from app.utils import insert_status


celery.conf.beat_schedule = {
    'collect': {
        'task': 'tasks.collect',
        'schedule': settings.POLLING_INTERVAL_SECONDS,
        'args': ()
    },
    'cleaner': {
        'task': 'tasks.cleaner',
        'schedule': 86400,  # 1 dia
        'args': ()
    },
}


@celery.task(name='tasks.collect')
def collect():
    servers = monitored_instance.objects.all().filter(active=True)
    for server in servers:
        try:
            start_time = time.time()
            heartbeat = requests.get(server.base_url + settings.HEARTBEAT_PATH)
            response_time_ms = int((time.time() - start_time) * 1000)
            if heartbeat.status_code == 200:
                try:
                    data = heartbeat.json()
                    serializer = moodle_hearbeatSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    insert_status(instance=server,
                                  status='SUCCESS',
                                  data=serializer.validated_data,
                                  response_time_ms=response_time_ms,
                                  http_status_code=heartbeat.status_code)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


@celery.task(name='tasks.cleaner')
def cleaner():
    days_to_keep = settings.CLEANUP_INTERVAL_DAYS
    try:
        with transaction.atomic():

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            records_to_delete = moodle_heartbeat.objects.filter(
                collected_at__lt=cutoff_date
            )
            count_to_delete = records_to_delete.count()
            if count_to_delete == 0:
                return {
                    'success': True,
                    'message': f'No se encontraron registros más antiguos de {days_to_keep} días',
                    'deleted_count': 0,
                    'days_to_keep': days_to_keep,
                    'cutoff_date': cutoff_date.isoformat(),
                    'remaining_count': moodle_heartbeat.objects.count(),
                    'config_used': 'custom' if custom_days is not None else 'settings'
                }


            deleted_info = records_to_delete.delete()
            total_deleted = deleted_info[0] if deleted_info else 0
            return {
                'success': True,
                'message': f'Se eliminaron {total_deleted} registros más antiguos de {days_to_keep} días',
                'deleted_count': total_deleted,
            }

    except moodle_heartbeat.DoesNotExist:
        return {
            'success': True,
            'message': 'No hay registros en la base de datos',
            'deleted_count': 0,
            'days_to_keep': days_to_keep,
            'remaining_count': 0
        }
    except Exception as e:
        print(e)
