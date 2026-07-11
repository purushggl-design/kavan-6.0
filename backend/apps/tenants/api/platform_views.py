from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import serializers as drf_serializers

from apps.tenants.permissions import IsPlatformAdmin
from apps.tenants.models.tenant import Tenant, TenantStatus
from apps.tenants.models.tenant_member import TenantMember, MemberRole, MemberStatus
from apps.tenants.serializers import TenantSerializer
from apps.tenants.services.tenant_lifecycle_service import TenantLifecycleService
from apps.authentication.models import UserStatus

User = get_user_model()


class PlatformTenantListView(APIView):
    """
    Platform Admin: List all tenants or create a new tenant.
    GET  /api/v1/platform/tenants/
    POST /api/v1/platform/tenants/
    """
    permission_classes = [IsPlatformAdmin]
    serializer_class = TenantSerializer

    @extend_schema(summary="List all tenants (Platform Admin)", responses={200: TenantSerializer(many=True)})
    def get(self, request):
        status_filter = request.query_params.get('status')
        qs = Tenant.unscoped.all().order_by('-created_at')
        if status_filter:
            qs = qs.filter(tenant_status=status_filter.upper())

        serializer = TenantSerializer(qs, many=True)
        return Response({'success': True, 'count': qs.count(), 'data': serializer.data})

    @extend_schema(summary="Create a new tenant (Platform Admin)", request=TenantSerializer, responses={201: TenantSerializer})
    def post(self, request):
        data = request.data

        required = ['tenant_code', 'tenant_name', 'company_name', 'company_domain']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return Response(
                {'success': False, 'error': f"Missing required fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Tenant.unscoped.filter(tenant_code=data['tenant_code']).exists():
            return Response(
                {'success': False, 'error': 'Tenant code already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Tenant.unscoped.filter(company_domain=data['company_domain']).exists():
            return Response(
                {'success': False, 'error': 'Company domain already registered.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tenant = Tenant.unscoped.create(
            tenant_code=data['tenant_code'],
            tenant_name=data['tenant_name'],
            company_name=data['company_name'],
            company_domain=data['company_domain'],
            company_email=data.get('company_email', ''),
            company_phone=data.get('company_phone', ''),
            timezone=data.get('timezone', 'UTC'),
            language=data.get('language', 'en'),
            currency=data.get('currency', 'USD'),
            tenant_status=TenantStatus.PENDING,
            owner=request.user,
        )
        return Response(
            {'success': True, 'data': TenantSerializer(tenant).data},
            status=status.HTTP_201_CREATED,
        )


class PlatformTenantDetailView(APIView):
    """
    Platform Admin: Get, update, or delete a specific tenant.
    GET    /api/v1/platform/tenants/<id>/
    PATCH  /api/v1/platform/tenants/<id>/
    DELETE /api/v1/platform/tenants/<id>/
    """
    permission_classes = [IsPlatformAdmin]
    serializer_class = TenantSerializer

    def _get_tenant(self, pk):
        try:
            return Tenant.unscoped.get(pk=pk)
        except Tenant.DoesNotExist:
            return None

    def get(self, request, pk):
        tenant = self._get_tenant(pk)
        if not tenant:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)
        data = TenantSerializer(tenant).data
        data['member_count'] = TenantMember.objects.filter(tenant=tenant).count()
        return Response({'success': True, 'data': data})

    def patch(self, request, pk):
        tenant = self._get_tenant(pk)
        if not tenant:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)

        editable_fields = ['tenant_name', 'company_name', 'company_email', 'company_phone',
                           'company_logo', 'timezone', 'language', 'currency']
        for field in editable_fields:
            if field in request.data:
                setattr(tenant, field, request.data[field])
        tenant.save()
        return Response({'success': True, 'data': TenantSerializer(tenant).data})

    def delete(self, request, pk):
        tenant = self._get_tenant(pk)
        if not tenant:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)
        TenantLifecycleService.delete_tenant(tenant)
        return Response({'success': True, 'message': 'Tenant deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PlatformTenantApproveView(APIView):
    """
    Approve a PENDING tenant → sets status to ACTIVE.
    POST /api/v1/platform/tenants/<id>/approve/
    """
    permission_classes = [IsPlatformAdmin]

    class _EmptySerializer(drf_serializers.Serializer):
        pass
    serializer_class = _EmptySerializer

    def post(self, request, pk):
        try:
            tenant = Tenant.unscoped.get(pk=pk)
        except Tenant.DoesNotExist:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)

        if tenant.tenant_status not in [TenantStatus.PENDING, TenantStatus.APPROVED]:
            return Response(
                {'success': False, 'error': f"Cannot approve a tenant with status '{tenant.tenant_status}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        TenantLifecycleService.activate_tenant(tenant)
        return Response({'success': True, 'message': 'Tenant approved and activated.', 'data': TenantSerializer(tenant).data})


class PlatformTenantSuspendView(APIView):
    """
    Suspend an ACTIVE tenant.
    POST /api/v1/platform/tenants/<id>/suspend/
    """
    permission_classes = [IsPlatformAdmin]

    class _ReasonSerializer(drf_serializers.Serializer):
        reason = drf_serializers.CharField(required=False, default='', allow_blank=True)
    serializer_class = _ReasonSerializer

    def post(self, request, pk):
        try:
            tenant = Tenant.unscoped.get(pk=pk)
        except Tenant.DoesNotExist:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)

        if tenant.tenant_status == TenantStatus.SUSPENDED:
            return Response({'success': False, 'error': 'Tenant is already suspended.'}, status=status.HTTP_400_BAD_REQUEST)

        reason = request.data.get('reason', '')
        TenantLifecycleService.suspend_tenant(tenant, reason=reason)
        return Response({'success': True, 'message': 'Tenant suspended.', 'data': TenantSerializer(tenant).data})


class PlatformTenantCreateAdminView(APIView):
    """
    Create a Tenant Admin user for an ACTIVE tenant.
    POST /api/v1/platform/tenants/<id>/create-admin/
    Body: { "email", "first_name", "last_name", "password" }
    """
    permission_classes = [IsPlatformAdmin]

    class _AdminSerializer(drf_serializers.Serializer):
        email = drf_serializers.EmailField()
        first_name = drf_serializers.CharField(max_length=150)
        last_name = drf_serializers.CharField(max_length=150)
        password = drf_serializers.CharField(min_length=8, write_only=True)
    serializer_class = _AdminSerializer

    @transaction.atomic
    def post(self, request, pk):
        try:
            tenant = Tenant.unscoped.get(pk=pk)
        except Tenant.DoesNotExist:
            return Response({'success': False, 'error': 'Tenant not found.'}, status=status.HTTP_404_NOT_FOUND)

        if tenant.tenant_status != TenantStatus.ACTIVE:
            return Response(
                {'success': False, 'error': 'Tenant must be ACTIVE before creating an admin.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.data.get('email')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        password = request.data.get('password')

        if not email or not password:
            return Response({'success': False, 'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'success': False, 'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user account
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            status=UserStatus.ACTIVE,
            email_verified=True,
        )

        # Link user to tenant as ADMIN member
        TenantMember.objects.create(
            tenant=tenant,
            user=user,
            role=MemberRole.ADMIN,
            status=MemberStatus.ACTIVE,
        )

        return Response({
            'success': True,
            'message': f"Tenant Admin '{email}' created and linked to '{tenant.tenant_name}'.",
            'data': {
                'user_id': str(user.id),
                'email': user.email,
                'tenant': tenant.tenant_name,
                'role': 'ADMIN',
            },
        }, status=status.HTTP_201_CREATED)
