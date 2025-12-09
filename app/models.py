from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class monitored_instance(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateField()
    updated_at = models.DateField()

    class Meta:
        verbose_name = 'Instancia de monitor'
        verbose_name_plural = 'Instancia de Monitores'

    def __str__(self):
        return self.name


class moodle_heartbeat(models.Model):
    monitored_instance = models.ForeignKey(monitored_instance, related_name='moodle_heartbeats', on_delete=models.SET_NULL, null=True, blank=True)
    disk_total_bytes = models.BigIntegerField(null=True)
    disk_used_bytes = models.BigIntegerField(null=True)
    disk_free_bytes = models.BigIntegerField(null=True)
    disk_used_percent = models.IntegerField(null=True)
    cpu_load = models.IntegerField(null=True)
    memory_total_bytes = models.BigIntegerField(null=True)
    memory_free_bytes = models.BigIntegerField(null=True)
    users = models.IntegerField(null=True)
    courses = models.IntegerField(null=True)
    unique_visitors = models.IntegerField(null=True)
    maintenance_mode = models.BooleanField()
    moodle_version = models.CharField(max_length=20)
    moodle_release = models.CharField(max_length=100)
    cron_last_run_timestamp = models.FloatField(null=True)
    cron_expected_frequency_minutes = models.IntegerField(null=True)
    collected_at = models.DateTimeField(default=timezone.now)
    system_timestamp = models.DateTimeField()
    status = models.CharField(max_length=100, null=True, blank=True)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    http_status_code = models.IntegerField(default=200, null=True)

    class Meta:
        verbose_name = 'Métrica de moodle'
        verbose_name_plural = 'Métricas de moodle'


class alert_rule(models.Model):
    monitored_instance = models.ForeignKey(monitored_instance, related_name='alert_rules', on_delete=models.SET_NULL, null=True, blank=True)
    metric_name = models.CharField(max_length=100)
    value = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Regla de Alerta'
        verbose_name_plural = 'Reglas de Alertas'

    def __str__(self):
        return '{}--{}'.format(self.monitored_instance.name, self.metric_name)


class alert(models.Model):
    server_name = models.CharField()
    monitored_instance = models.ForeignKey(monitored_instance, related_name='alerts', on_delete=models.SET_NULL, null=True)
    alert_type = models.CharField()
    message = models.CharField()
    severity = models.CharField
    created_at = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'

    def __str__(self):
        return self.server_name


class User(AbstractUser):
    last_login = None

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.last_name)
