from celery import shared_task
from apps.deployments.models import Deployment, DeploymentJob
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.services.provision_service import ProvisionService
from apps.deployments.services.rollback_service import RollbackService
from apps.deployments.services.upgrade_service import UpgradeService
from apps.deployments.services.health_service import HealthService
from apps.deployments.providers.docker_provider import DockerProvider

@shared_task(bind=True, max_retries=3)
def deploy_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    provider = DockerProvider()
    try:
        service = ProvisionService(provider=provider)
        service.provision(deployment, job)
    except Exception as exc:
        StateMachineService().transition(deployment, 'FAILED', job)
        rollback_product_task.delay(deployment_id, job_id)
        self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def rollback_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.filter(id=job_id).first()
    provider = DockerProvider()
    service = RollbackService(provider=provider)
    service.rollback(deployment, job)

@shared_task
def restart_product_task(deployment_id):
    deployment = Deployment.objects.get(id=deployment_id)
    provider = DockerProvider()
    provider.restart_infrastructure(deployment)

@shared_task
def upgrade_product_task(deployment_id, job_id, new_version_tag):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    UpgradeService().upgrade(deployment, job, new_version_tag)

@shared_task
def health_check_task():
    provider = DockerProvider()
    service = HealthService(provider=provider)
    for deployment in Deployment.objects.filter(status='RUNNING'):
        is_healthy = service.check_health(deployment)
        # Handle unhealthy status based on requirements

@shared_task
def cleanup_failed_task():
    pass

@shared_task
def deployment_timeout_task():
    pass
