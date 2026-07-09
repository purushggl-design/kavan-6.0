from rest_framework import serializers
from apps.devices.models import TrustedDevice

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedDevice
        fields = [
            'id', 'device_name', 'device_type', 'os', 'browser',
            'ip_address', 'is_trusted', 'last_seen_at', 'created_at'
        ]
        read_only_fields = fields
