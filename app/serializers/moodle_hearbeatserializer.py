from rest_framework import serializers
from app.models import moodle_heartbeat


class moodle_hearbeatSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField(required=True)
    disk = serializers.JSONField(required=True)
    cpu_load = serializers.IntegerField(required=True)
    memory = serializers.JSONField(required=True)
    users = serializers.IntegerField(required=True)
    courses = serializers.IntegerField(required=True)
    unique_visitors = serializers.IntegerField(required=True)
    maintenance_mode = serializers.BooleanField()
    moodle_version = serializers.CharField(required=True)
    moodle_release = serializers.CharField(required=True)
    cron = serializers.JSONField(required=True)

    class Meta:
        model = moodle_heartbeat
        fields = '__all__'
