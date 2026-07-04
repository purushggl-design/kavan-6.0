import logging
from apps.deployments.models import DeploymentState
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class ProvisionService:
    def __init__(self, provider: ProvisionProvider = None):
        self.provider = provider
        
    def provision(self, deployment, job):
        logger.info(f"Provisioning for {deployment.id}")
        StateMachineService.transition(deployment, DeploymentState.PROVISIONING, job)
        
        if self.provider:
            self.provider.provision_infrastructure(deployment)
            
        StateMachineService.transition(deployment, DeploymentState.INSTALLING, job)
        StateMachineService.transition(deployment, DeploymentState.CONFIGURING, job)
        StateMachineService.transition(deployment, DeploymentState.STARTING, job)
        StateMachineService.transition(deployment, DeploymentState.RUNNING, job)
        return True
