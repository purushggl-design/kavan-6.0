from rest_framework import serializers
from apps.profiles.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'avatar_url', 'bio', 'timezone', 'language', 'date_format',
            'email_notifications', 'push_notifications', 'marketing_emails'
        ]
        read_only_fields = ['id']
