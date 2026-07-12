from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.integrations.models.siem import SIEMIntegrationConfig, SIEMRetryQueue
from .serializers import SIEMIntegrationConfigSerializer, SIEMRetryQueueSerializer

class SIEMIntegrationConfigViewSet(viewsets.ModelViewSet):
    queryset = SIEMIntegrationConfig.objects.all()
    serializer_class = SIEMIntegrationConfigSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "SIEM Integration configs retrieved successfully.",
            "data": serializer.data,
            "errors": None,
            "meta": {"count": queryset.count()}
        })
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "SIEM Integration config created successfully.",
                "data": serializer.data,
                "errors": None,
                "meta": {}
            }, status=201)
        return Response({
            "success": False,
            "message": "Validation Failed",
            "data": None,
            "errors": serializer.errors,
            "meta": {}
        }, status=400)

class SIEMRetryQueueViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SIEMRetryQueue.objects.all()
    serializer_class = SIEMRetryQueueSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Retry queue retrieved successfully.",
            "data": serializer.data,
            "errors": None,
            "meta": {"count": queryset.count()}
        })
