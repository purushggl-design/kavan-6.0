from rest_framework import serializers
from apps.monitoring.models.events import Event
from apps.monitoring.models.metrics import Metric, HealthCheck

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"

class HealthCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheck
        fields = "__all__"
