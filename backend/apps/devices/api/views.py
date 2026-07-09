from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from common.responses.standard_response import StandardResponse
from apps.devices.services.device_service import DeviceService
from apps.devices.api.serializers import DeviceSerializer
from apps.rbac.permissions.decorators import HasPlatformPermission

class DeviceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = DeviceService()
        
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), HasPlatformPermission("devices:view")()]
        if self.action == 'destroy':
            return [IsAuthenticated(), HasPlatformPermission("devices:delete")()]
        return super().get_permissions()
        
    @extend_schema(summary="List My Devices", responses={200: DeviceSerializer(many=True)})
    def list(self, request):
        devices = self.service.get_user_devices(request.user.id)
        serializer = DeviceSerializer(devices, many=True)
        return StandardResponse.success(data=serializer.data)
        
    @extend_schema(summary="Delete Device", responses={200: StandardResponse})
    def destroy(self, request, pk=None):
        self.service.delete_device(request.user.id, pk)
        return StandardResponse.success(message="Device deleted successfully.")
