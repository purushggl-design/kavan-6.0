from rest_framework import serializers

class MFAVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)

class MFASetupResponseSerializer(serializers.Serializer):
    secret = serializers.CharField()
    qr_code_url = serializers.CharField()
    backup_codes = serializers.ListField(child=serializers.CharField())
