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
        verbose_name = 'monitored instance'
        verbose_name_plural = 'monitored instances'

    def __str__(self):
        return self.name


class moodle_heartbeat(models.Model):
    monitored_instance = models.ForeignKey(monitored_instance, related_name='moodle_heartbeats', on_delete=models.SET_NULL, null=True)
    disk_total_bytes = models.BigIntegerField()
    disk_used_bytes = models.BigIntegerField()
    disk_free_bytes = models.BigIntegerField()
    disk_used_percent = models.IntegerField()
    cpu_load = models.IntegerField()
    memory_total_bytes = models.BigIntegerField()
    memory_free_bytes = models.BigIntegerField()
    users = models.IntegerField()
    courses = models.IntegerField()
    unique_visitors = models.IntegerField()
    maintenance_mode = models.BooleanField()
    moodle_version = models.CharField(max_length=20)
    moodle_release = models.CharField(max_length=100)
    cron_last_run_timestamp = models.FloatField()
    cron_expected_frequency_minutes = models.IntegerField()
    collected_at = models.DateTimeField(default=timezone.now)
    system_timestamp = models.DateTimeField()

    class Meta:
        verbose_name = 'moodle-heartbeat'
        verbose_name_plural = 'moodle-heartbeats'


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
