from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.deployments.models import Deployment
from apps.deployments.services.deployment_service import DeploymentService

class TenantDeploymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tenant APIs for managing their own deployments.
    """
    queryset = Deployment.objects.none() # Scoped via middleware in reality

    @extend_schema(summary="Deploy Product manually")
    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        deployment = self.get_object()
        try:
            job = DeploymentService.deploy(deployment)
            return Response({"status": "Deploying", "job_id": str(job.id)})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Get Deployment Status")
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        deployment = self.get_object()
        return Response({"status": deployment.status})

    @extend_schema(summary="Restart Deployment")
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        return Response({"status": "Restart requested"})
