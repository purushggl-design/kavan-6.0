from rest_framework import serializers
from apps.authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'status', 
            'mfa_enabled', 'last_login_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'status', 'mfa_enabled', 'last_login_at', 'created_at', 'updated_at']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
