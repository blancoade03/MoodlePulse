from datetime import datetime, timezone
from app.models import moodle_heartbeat
# import logging
#
# logger = logging.getLogger(__name__)


def insert_status(instance, data, status, error_message='', http_status_code=0, response_time_ms=0):
    """
    Inserta un registro de estado en la tabla moodle_heartbeat usando Django ORM.
    """
    try:

        # Inicializar el diccionario de datos para el modelo
        heartbeat_data = {
            'instance': instance,
            'status': status,
            'error_message': error_message,
            'response_time_ms': response_time_ms,
            'http_status_code': http_status_code,
        }

        # Extraer datos solo si `data` es un diccionario válido
        if data:
            # Timestamp del sistema
            if 'timestamp' in data:
                try:
                    heartbeat_data['system_timestamp'] = datetime.fromtimestamp(
                        data['timestamp'], tz=timezone.utc
                    )
                except (ValueError, OSError, TypeError) as e:
                    print(f"⚠️ [{instance.name}] Timestamp inválido: {e}")

            # Métricas de disco
            if 'disk' in data:
                heartbeat_data.update({
                    'disk_total_bytes': data['disk'].get('total_bytes'),
                    'disk_used_bytes': data['disk'].get('used_bytes'),
                    'disk_free_bytes': data['disk'].get('free_bytes'),
                    'disk_used_percent': data['disk'].get('used_percent'),
                })

            # Métricas de memoria
            if 'memory' in data:
                heartbeat_data.update({
                    'memory_total_bytes': data['memory'].get('total_bytes'),
                    'memory_free_bytes': data['memory'].get('free_bytes'),
                })

            # Métricas de CPU
            heartbeat_data['cpu_load'] = data.get('cpu_load')

            # Métricas de Moodle
            heartbeat_data.update({
                'users': data.get('users'),
                'courses': data.get('courses'),
                'unique_visitors': data.get('unique_visitors'),
                'maintenance_mode': data.get('maintenance_mode'),
                'moodle_version': data.get('moodle_version'),
                'moodle_release': data.get('moodle_release'),
            })

            # Métricas de cron
            if 'cron' in data:
                cron_last_run = data['cron'].get('last_run_timestamp')
                if cron_last_run:
                    try:
                        heartbeat_data['cron_last_run_timestamp'] = cron_last_run
                    except (ValueError, OSError, TypeError) as e:
                        print(f"⚠️ [{instance.name}] Timestamp de cron inválido: {e}")

                heartbeat_data['cron_expected_frequency_minutes'] = data['cron'].get(
                    'expected_frequency_minutes'
                )

        # Crear el registro usando el ORM
        heartbeat = moodle_heartbeat.objects.create(
            monitored_instance=heartbeat_data.get('instance', 0),  # Asegúrate que el campo en el modelo se llame así
            status=heartbeat_data.get('status', 0),
            error_message=heartbeat_data.get('error_message'),
            response_time_ms=heartbeat_data.get('response_time_ms'),
            http_status_code=heartbeat_data.get('http_status_code'),

                # Campos de disco
            disk_total_bytes=heartbeat_data.get('disk_total_bytes', 0),
            disk_used_bytes=heartbeat_data.get('disk_used_bytes', 0),
            disk_free_bytes=heartbeat_data.get('disk_free_bytes', 0),
            disk_used_percent=heartbeat_data.get('disk_used_percent', 0),

                # Campos de CPU y memoria
            cpu_load=heartbeat_data.get('cpu_load', 0),
            memory_total_bytes=heartbeat_data.get('memory_total_bytes', 0),
            memory_free_bytes=heartbeat_data.get('memory_free_bytes', 0),

                # Campos de métricas de Moodle
            users=heartbeat_data.get('users', 0),
            courses=heartbeat_data.get('courses', 0),
            unique_visitors=heartbeat_data.get('unique_visitors', 0),
            maintenance_mode=heartbeat_data.get('maintenance_mode'),
            moodle_version=heartbeat_data.get('moodle_version'),
            moodle_release=heartbeat_data.get('moodle_release'),

                # Campos de cron
            cron_last_run_timestamp=heartbeat_data.get('cron_last_run_timestamp', 0),
            cron_expected_frequency_minutes=heartbeat_data.get('cron_expected_frequency_minutes', 0),

                # Campos de timestamp
            system_timestamp=datetime.fromtimestamp(heartbeat_data.get('timestamp', 0), tz=timezone.utc),
        )

        print(f"✅ [{instance.name}] Estado registrado: {status}")
        return heartbeat

    except Exception as e:
        print(f"❌ [{instance.name}] Error al guardar estado: {e}")