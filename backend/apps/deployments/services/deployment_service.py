import logging
from apps.deployments.repositories import (
    DeploymentRepository, DeploymentJobRepository, DeploymentHistoryRepository,
    DeploymentLogRepository
)
from apps.deployments.models import DeploymentState

logger = logging.getLogger(__name__)

class StateMachineService:
    VALID_TRANSITIONS = {
        DeploymentState.REQUESTED: [DeploymentState.QUEUED, DeploymentState.FAILED],
        DeploymentState.QUEUED: [DeploymentState.VALIDATING, DeploymentState.FAILED],
        DeploymentState.VALIDATING: [DeploymentState.PROVISIONING, DeploymentState.FAILED],
        DeploymentState.PROVISIONING: [DeploymentState.INSTALLING, DeploymentState.FAILED],
        DeploymentState.INSTALLING: [DeploymentState.CONFIGURING, DeploymentState.FAILED],
        DeploymentState.CONFIGURING: [DeploymentState.STARTING, DeploymentState.FAILED],
        DeploymentState.STARTING: [DeploymentState.HEALTH_CHECK, DeploymentState.FAILED],
        DeploymentState.HEALTH_CHECK: [DeploymentState.RUNNING, DeploymentState.FAILED],
        DeploymentState.RUNNING: [DeploymentState.FAILED, DeploymentState.ROLLBACK],
        DeploymentState.FAILED: [DeploymentState.ROLLBACK],
        DeploymentState.ROLLBACK: [DeploymentState.ROLLED_BACK, DeploymentState.FAILED],
        DeploymentState.ROLLED_BACK: [],
    }

    @staticmethod
    def transition(deployment, new_status, job=None):
        old_status = deployment.status
        if old_status == new_status:
            return
            
        if new_status not in StateMachineService.VALID_TRANSITIONS.get(old_status, []):
            raise ValueError(f"Invalid transition from {old_status} to {new_status}")
            
        DeploymentRepository.update_status(deployment.id, new_status)
        DeploymentHistoryRepository.create(deployment.id, old_status, new_status)
        
        deployment.status = new_status
        
        if job:
            DeploymentJobRepository.update_status(job.id, new_status)
            DeploymentLogRepository.append_log(job.id, f"Transitioned from {old_status} to {new_status}")
            job.status = new_status
            
        logger.info(f"Deployment {deployment.id} transitioned {old_status} -> {new_status}")

class SchedulerService:
    @staticmethod
    def schedule_deployment(deployment):
        job = DeploymentJobRepository.create(deployment.id, status=DeploymentState.QUEUED)
        StateMachineService.transition(deployment, DeploymentState.QUEUED, job)
        return job

class DeploymentService:
    @staticmethod
    def request_deployment(tenant, product, tenant_product, template):
        deployment = DeploymentRepository.create(
            tenant=tenant, product=product, tenant_product=tenant_product, template=template
        )
        return deployment

    @staticmethod
    def deploy(deployment):
        if deployment.status != DeploymentState.REQUESTED:
            raise ValueError(f"Cannot deploy from state {deployment.status}")
            
        job = SchedulerService.schedule_deployment(deployment)
        
        # Trigger Celery Task
        from apps.deployments.tasks import deploy_product_task
        deploy_product_task.delay(deployment.id, job.id)
        
        return job
