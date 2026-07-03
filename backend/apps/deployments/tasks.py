from celery import shared_task
from apps.deployments.models import Deployment, DeploymentJob
from apps.deployments.services import (
    ProvisionService, RollbackService, UpgradeService, HealthService, StateMachineService
)

@shared_task(bind=True, max_retries=3)
def deploy_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    try:
        ProvisionService.provision(deployment, job)
    except Exception as exc:
        StateMachineService.transition(deployment, 'FAILED', job)
        self.retry(exc=exc, countdown=60)

@shared_task(bind=True)
def rollback_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    RollbackService.rollback(deployment, job)

@shared_task
def restart_product_task(deployment_id):
    pass

@shared_task
def upgrade_product_task(deployment_id, job_id, new_version_tag):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    UpgradeService.upgrade(deployment, job, new_version_tag)

@shared_task
def health_check_task():
    for deployment in Deployment.objects.filter(status='RUNNING'):
        HealthService.check_health(deployment)

@shared_task
def cleanup_failed_task():
    pass

@shared_task
def deployment_timeout_task():
    pass

@shared_task
def deployment_notification_task():
    pass
