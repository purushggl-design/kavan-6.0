import logging
from common.services.base_service import BaseService
from apps.deployments.models import DeploymentState
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class RollbackService(BaseService):
    def __init__(self, provider: ProvisionProvider = None):
        super().__init__()
        self.provider = provider

    def rollback(self, deployment, job):
        self._log_operation("rollback", deployment_id=str(deployment.id))
        
        state_machine = StateMachineService()
        state_machine.transition(deployment, DeploymentState.ROLLBACK, job)
        
        if self.provider:
            self.provider.rollback_infrastructure(deployment)
            
        state_machine.transition(deployment, DeploymentState.ROLLED_BACK, job)
        return True
