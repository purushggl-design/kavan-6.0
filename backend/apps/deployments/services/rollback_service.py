import logging
from apps.deployments.models import DeploymentState
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class RollbackService:
    def __init__(self, provider: ProvisionProvider = None):
        self.provider = provider

    def rollback(self, deployment, job):
        logger.info(f"Rolling back deployment {deployment.id}")
        StateMachineService.transition(deployment, DeploymentState.ROLLBACK, job)
        
        if self.provider:
            self.provider.rollback_infrastructure(deployment)
            
        StateMachineService.transition(deployment, DeploymentState.ROLLED_BACK, job)
        return True
