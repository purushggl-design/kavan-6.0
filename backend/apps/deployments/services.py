import logging
from apps.deployments.repositories import (
    DeploymentRepository, DeploymentJobRepository, DeploymentHistoryRepository,
    DeploymentLogRepository, DeploymentArtifactRepository
)
from apps.deployments.models import DeploymentState

logger = logging.getLogger(__name__)

class StateMachineService:
    # Defined valid next states for each state
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
        
        if job:
            DeploymentJobRepository.update_status(job.id, new_status)
            DeploymentLogRepository.append_log(job.id, f"Transitioned from {old_status} to {new_status}")
            
        logger.info(f"Deployment {deployment.id} transitioned {old_status} -> {new_status}")

from abc import ABC, abstractmethod

class ProvisionProvider(ABC):
    @abstractmethod
    def provision_infrastructure(self, deployment):
        pass

class ProvisionService:
    def __init__(self, provider: ProvisionProvider = None):
        self.provider = provider
        
    def provision(self, deployment, job):
        logger.info(f"Mock Provisioning for {deployment.id}")
        StateMachineService.transition(deployment, DeploymentState.PROVISIONING, job)
        
        if self.provider:
            self.provider.provision_infrastructure(deployment)
            
        StateMachineService.transition(deployment, DeploymentState.INSTALLING, job)
        StateMachineService.transition(deployment, DeploymentState.CONFIGURING, job)
        StateMachineService.transition(deployment, DeploymentState.STARTING, job)
        StateMachineService.transition(deployment, DeploymentState.RUNNING, job)
        return True

class RollbackService:
    @staticmethod
    def rollback(deployment, job):
        logger.info(f"Rolling back deployment {deployment.id}")
        StateMachineService.transition(deployment, DeploymentState.ROLLBACK, job)
        StateMachineService.transition(deployment, DeploymentState.ROLLED_BACK, job)
        return True

class UpgradeService:
    @staticmethod
    def upgrade(deployment, job, new_version_tag):
        logger.info(f"Upgrading deployment {deployment.id} to {new_version_tag}")
        # Logic to upgrade (stop, patch, start)
        return True

class HealthService:
    @staticmethod
    def check_health(deployment):
        logger.info(f"Checking health for deployment {deployment.id}")
        # Determine health (stubbed)
        return True

class ArtifactService:
    @staticmethod
    def attach_artifact(deployment, s3_url, artifact_type):
        return DeploymentArtifactRepository.create(deployment.id, s3_url, artifact_type)

class SchedulerService:
    @staticmethod
    def schedule_deployment(deployment):
        job = DeploymentJobRepository.create(deployment.id, status=DeploymentState.QUEUED)
        StateMachineService.transition(deployment, DeploymentState.QUEUED, job)
        return job

class DeploymentService:
    @staticmethod
    def request_deployment(tenant, product, template):
        deployment = DeploymentRepository.create(tenant=tenant, product=product, template=template)
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
