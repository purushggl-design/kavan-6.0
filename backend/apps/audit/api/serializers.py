from rest_framework import serializers
from apps.audit.models import AuditEvent

class AuditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEvent
        fields = '__all__'
        read_only_fields = ['id', 'user', 'user_email', 'event_type', 'success', 'failure_reason', 'ip_address', 'user_agent', 'device_id', 'location', 'metadata', 'tenant_id', 'created_at']
