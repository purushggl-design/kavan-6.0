from rest_framework import serializers
from apps.incidents.models.incidents import Alert, Incident, IncidentActivity


class AlertSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'title', 'description',
            'severity', 'severity_display',
            'status', 'status_display',
            'rule_name', 'event_data',
            'tenant_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'event_data', 'rule_name']


class IncidentActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = IncidentActivity
        fields = ['id', 'action', 'notes', 'user_email', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None


class IncidentSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    alert_count = serializers.SerializerMethodField()
    assigned_to_email = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = [
            'id', 'title', 'description',
            'severity', 'severity_display',
            'status', 'status_display',
            'tenant_id', 'alert_count',
            'assigned_to', 'assigned_to_email',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_alert_count(self, obj):
        return obj.alerts.count()

    def get_assigned_to_email(self, obj):
        return obj.assigned_to.email if obj.assigned_to else None


class IncidentDetailSerializer(IncidentSerializer):
    """Extended serializer with activities for the detail view."""
    activities = IncidentActivitySerializer(many=True, read_only=True)
    alerts = AlertSerializer(many=True, read_only=True)

    class Meta(IncidentSerializer.Meta):
        fields = IncidentSerializer.Meta.fields + ['activities', 'alerts']
