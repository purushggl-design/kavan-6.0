from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from common.responses.standard_response import StandardResponse
from apps.rbac.permissions.decorators import HasPlatformPermission
from apps.audit.repositories.audit_repository import AuditRepository
from apps.audit.api.serializers import AuditEventSerializer

class AuditViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = AuditRepository()
        
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), HasPlatformPermission("audit:view")()]
        return super().get_permissions()
        
    @extend_schema(summary="List Audit Events", responses={200: AuditEventSerializer(many=True)})
    def list(self, request):
        events = self.repo.get_events_for_user(request.user.id)
        serializer = AuditEventSerializer(events, many=True)
        return StandardResponse.success(data=serializer.data)
