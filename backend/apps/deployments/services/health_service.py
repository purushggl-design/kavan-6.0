import logging
from common.services.base_service import BaseService
from apps.deployments.models import DeploymentState
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class HealthService(BaseService):
    def __init__(self, provider: ProvisionProvider = None):
        super().__init__()
        self.provider = provider

    def check_health(self, deployment):
        self._log_operation("check_health", deployment_id=str(deployment.id))
        if self.provider:
            return self.provider.health_check(deployment)
        return True
