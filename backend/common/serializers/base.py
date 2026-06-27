"""
KAVAN v6.0 — Base Serializer
"""

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for all KAVAN model serializers.

    Marks id, created_at, updated_at as read-only.
    Subclasses should define Meta.model and Meta.fields.
    """

    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BaseReadSerializer(serializers.Serializer):
    """
    Base serializer for read-only response serialization.
    Use when the response doesn't map 1:1 to a model.
    """
    pass


class BaseWriteSerializer(serializers.Serializer):
    """
    Base serializer for write operations (create/update).
    Provides common validation hooks.
    """

    def validate(self, attrs):
        """Global cross-field validation hook."""
        return super().validate(attrs)
