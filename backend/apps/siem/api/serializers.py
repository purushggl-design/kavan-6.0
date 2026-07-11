from rest_framework import serializers
from apps.siem.models.rules import DetectionRule, CorrelationRule


class DetectionRuleSerializer(serializers.ModelSerializer):
    rule_type_display = serializers.CharField(source='get_rule_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = DetectionRule
        fields = [
            'id', 'name', 'description',
            'rule_type', 'rule_type_display',
            'conditions', 'threshold', 'time_window_seconds',
            'severity', 'severity_display',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CorrelationRuleSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = CorrelationRule
        fields = [
            'id', 'name', 'description',
            'sequence', 'time_window_seconds',
            'severity', 'severity_display',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
