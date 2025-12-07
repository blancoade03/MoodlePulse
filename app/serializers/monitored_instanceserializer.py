from rest_framework import serializers
from app.models import monitored_instance


class MonitoredInstanceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    base_url = serializers.CharField(max_length=100)

    class Meta:
        model = monitored_instance
        fields = '__all__'
