from rest_framework import serializers
from apps.rbac.models.platform_rbac import PlatformPermission, PlatformRolePermission
from apps.rbac.models.tenant_rbac import TenantPermission, RolePermission, TenantRole


class PlatformPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformPermission
        fields = ['id', 'code', 'description']
        read_only_fields = ['id']


class PlatformRolePermissionSerializer(serializers.ModelSerializer):
    permission_detail = PlatformPermissionSerializer(source='permission', read_only=True)

    class Meta:
        model = PlatformRolePermission
        fields = ['id', 'role', 'permission', 'permission_detail']
        read_only_fields = ['id']


class TenantPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantPermission
        fields = ['id', 'code', 'description']
        read_only_fields = ['id']


class RolePermissionSerializer(serializers.ModelSerializer):
    permission_detail = TenantPermissionSerializer(source='permission', read_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'permission_detail']
        read_only_fields = ['id']


class EffectivePermissionsSerializer(serializers.Serializer):
    """Read-only response: lists the calling user's effective permissions."""
    user_id = serializers.UUIDField()
    platform_role = serializers.CharField(allow_null=True)
    platform_permissions = serializers.ListField(child=serializers.CharField())
    tenant_id = serializers.UUIDField(allow_null=True)
    tenant_permissions = serializers.ListField(child=serializers.CharField())
