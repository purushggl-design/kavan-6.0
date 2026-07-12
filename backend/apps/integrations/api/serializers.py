from rest_framework import serializers
from apps.integrations.models.siem import SIEMIntegrationConfig, SIEMRetryQueue

class SIEMIntegrationConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIEMIntegrationConfig
        fields = ['id', 'provider', 'endpoint_url', 'is_active', 'min_severity_to_forward', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SIEMRetryQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIEMRetryQueue
        fields = ['id', 'provider', 'retry_count', 'last_error', 'next_retry_at', 'created_at']
        read_only_fields = ['id', 'created_at']
