from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.deployments.models import Deployment

class PlatformDeploymentViewSet(viewsets.ModelViewSet):
    """
    Platform APIs for managing all deployments in the KAVAN ecosystem.
    """
    queryset = Deployment.objects.all()

    @extend_schema(summary="Deploy Product manually")
    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        return Response({"status": "Deploying"})

    @extend_schema(summary="Rollback Deployment")
    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        return Response({"status": "Rolling back"})

    @extend_schema(summary="Upgrade Deployment")
    @action(detail=True, methods=['post'])
    def upgrade(self, request, pk=None):
        return Response({"status": "Upgrading"})
        
    @extend_schema(summary="Restart Deployment")
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        return Response({"status": "Restarting"})

class TenantDeploymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tenant APIs for managing their own deployments.
    """
    queryset = Deployment.objects.none() # Scoped via middleware in reality

    @extend_schema(summary="Get Deployment Status")
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        return Response({"status": "RUNNING"})

    @extend_schema(summary="Restart Deployment")
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        return Response({"status": "Restart requested"})
