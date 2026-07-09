import logging
from common.services.base_service import BaseService
from apps.deployments.models import DeploymentState
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class ProvisionService(BaseService):
    def __init__(self, provider: ProvisionProvider = None):
        super().__init__()
        self.provider = provider
        
    def provision(self, deployment, job):
        self._log_operation("provision", deployment_id=str(deployment.id))
        
        state_machine = StateMachineService()
        state_machine.transition(deployment, DeploymentState.PROVISIONING, job)
        
        if self.provider:
            self.provider.provision_infrastructure(deployment)
            
        state_machine.transition(deployment, DeploymentState.INSTALLING, job)
        state_machine.transition(deployment, DeploymentState.CONFIGURING, job)
        state_machine.transition(deployment, DeploymentState.STARTING, job)
        state_machine.transition(deployment, DeploymentState.RUNNING, job)
        return True
