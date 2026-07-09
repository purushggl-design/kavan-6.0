"""
KAVAN v6.0 — RBAC API Views
============================================================
Exposes:
  GET  /api/v1/rbac/my-permissions/         → caller's effective permissions
  GET  /api/v1/rbac/platform-permissions/   → list all platform permissions (SUPER_ADMIN)
  POST /api/v1/rbac/platform-permissions/   → create platform permission (SUPER_ADMIN)
  GET  /api/v1/rbac/role-assignments/       → list platform role → permission assignments (SUPER_ADMIN)
  POST /api/v1/rbac/role-assignments/       → assign permission to platform role (SUPER_ADMIN)
  DEL  /api/v1/rbac/role-assignments/{id}/  → remove role assignment (SUPER_ADMIN)

All platform-admin endpoints are protected by HasPlatformPermission.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.rbac.models.platform_rbac import PlatformPermission, PlatformRolePermission
from apps.rbac.models.tenant_rbac import TenantPermission, RolePermission
from apps.rbac.permissions.decorators import HasPlatformPermission
from apps.rbac.services.rbac_service import RBACService
from apps.rbac.api.serializers import (
    PlatformPermissionSerializer,
    PlatformRolePermissionSerializer,
    TenantPermissionSerializer,
    RolePermissionSerializer,
    EffectivePermissionsSerializer,
)
from common.responses.standard_response import StandardResponse

# Reusable permission class: only SUPER_ADMIN or users with rbac:manage permission
_PlatformRBACAdmin = HasPlatformPermission("rbac:manage")()


class RBACViewSet(viewsets.ViewSet):
    """
    Unified RBAC ViewSet.

    my-permissions: Any authenticated user — returns their own effective permissions.
    All other routes require rbac:manage platform permission (SUPER_ADMIN implicitly has it).
    """

    @extend_schema(
        summary="Get my effective permissions",
        description="Returns the calling user's platform role and computed permissions.",
        responses={200: EffectivePermissionsSerializer},
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated], url_path="my-permissions")
    def my_permissions(self, request):
        user = request.user
        platform_perms = []
        if user.platform_role:
            platform_perms = list(
                PlatformRolePermission.objects.filter(role=user.platform_role)
                .values_list("permission__code", flat=True)
            )
        # Tenant permissions (resolve from request.tenant if middleware sets it)
        tenant = getattr(request, "tenant", None)
        tenant_perms = []
        if tenant:
            from apps.tenants.models.tenant_member import TenantMember
            member = TenantMember.objects.filter(user=user, tenant=tenant, status="ACTIVE").first()
            if member:
                tenant_perms = list(
                    RolePermission.objects.filter(role=member.role)
                    .values_list("permission__code", flat=True)
                )
        data = {
            "user_id": user.id,
            "platform_role": user.platform_role,
            "platform_permissions": platform_perms,
            "tenant_id": tenant.id if tenant else None,
            "tenant_permissions": tenant_perms,
        }
        return StandardResponse.success(data=data, message="Effective permissions retrieved.")

    # ── Platform Permissions CRUD ─────────────────────────────────────────────

    @extend_schema(
        summary="List platform permissions",
        description="Requires rbac:manage permission.",
        responses={200: PlatformPermissionSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], permission_classes=[_PlatformRBACAdmin], url_path="platform-permissions")
    def list_platform_permissions(self, request):
        qs = PlatformPermission.objects.all().order_by("code")
        serializer = PlatformPermissionSerializer(qs, many=True)
        return StandardResponse.success(data=serializer.data)

    @extend_schema(
        summary="Create platform permission",
        description="Requires rbac:manage permission.",
        request=PlatformPermissionSerializer,
        responses={201: PlatformPermissionSerializer},
    )
    @action(detail=False, methods=["post"], permission_classes=[_PlatformRBACAdmin], url_path="platform-permissions/create")
    def create_platform_permission(self, request):
        serializer = PlatformPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return StandardResponse.success(data=serializer.data, message="Permission created.", status=status.HTTP_201_CREATED)

    # ── Role Assignments ──────────────────────────────────────────────────────

    @extend_schema(
        summary="List platform role→permission assignments",
        description="Requires rbac:manage permission.",
        responses={200: PlatformRolePermissionSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], permission_classes=[_PlatformRBACAdmin], url_path="role-assignments")
    def list_role_assignments(self, request):
        role_filter = request.query_params.get("role")
        qs = PlatformRolePermission.objects.select_related("permission").all()
        if role_filter:
            qs = qs.filter(role=role_filter)
        serializer = PlatformRolePermissionSerializer(qs, many=True)
        return StandardResponse.success(data=serializer.data)

    @extend_schema(
        summary="Assign permission to platform role",
        description="Requires rbac:manage permission.",
        request=PlatformRolePermissionSerializer,
        responses={201: PlatformRolePermissionSerializer},
    )
    @action(detail=False, methods=["post"], permission_classes=[_PlatformRBACAdmin], url_path="role-assignments/assign")
    def assign_role_permission(self, request):
        serializer = PlatformRolePermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj, created = PlatformRolePermission.objects.get_or_create(
            role=serializer.validated_data["role"],
            permission=serializer.validated_data["permission"],
        )
        return StandardResponse.success(
            data=PlatformRolePermissionSerializer(obj).data,
            message="Assignment created." if created else "Already exists.",
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Revoke permission from platform role",
        description="Requires rbac:manage permission.",
        responses={204: OpenApiResponse(description="Deleted")},
    )
    @action(detail=True, methods=["delete"], permission_classes=[_PlatformRBACAdmin], url_path="role-assignments")
    def revoke_role_permission(self, request, pk=None):
        try:
            assignment = PlatformRolePermission.objects.get(pk=pk)
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlatformRolePermission.DoesNotExist:
            return StandardResponse.error("Not found", status=status.HTTP_404_NOT_FOUND)
