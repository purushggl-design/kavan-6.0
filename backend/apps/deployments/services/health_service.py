import logging
from apps.deployments.models import DeploymentState
from apps.deployments.providers.base import ProvisionProvider

logger = logging.getLogger(__name__)

class HealthService:
    def __init__(self, provider: ProvisionProvider = None):
        self.provider = provider

    def check_health(self, deployment):
        logger.info(f"Checking health for deployment {deployment.id}")
        if self.provider:
            return self.provider.health_check(deployment)
        return True
