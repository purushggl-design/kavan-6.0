from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.deployments.models import Deployment
from apps.deployments.services.deployment_service import DeploymentService

class PlatformDeploymentViewSet(viewsets.ModelViewSet):
    """
    Platform APIs for managing all deployments in the KAVAN ecosystem.
    """
    queryset = Deployment.objects.all()

    @extend_schema(summary="Deploy Product manually")
    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        deployment = self.get_object()
        try:
            job = DeploymentService.deploy(deployment)
            return Response({"status": "Deploying", "job_id": str(job.id)})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Rollback Deployment")
    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        from apps.deployments.tasks import rollback_product_task
        deployment = self.get_object()
        rollback_product_task.delay(deployment.id, None) 
        return Response({"status": "Rolling back"})

    @extend_schema(summary="Upgrade Deployment")
    @action(detail=True, methods=['post'])
    def upgrade(self, request, pk=None):
        return Response({"status": "Upgrading"})
        
    @extend_schema(summary="Restart Deployment")
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        return Response({"status": "Restarting"})
