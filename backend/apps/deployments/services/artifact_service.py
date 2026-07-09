from common.services.base_service import BaseService
from apps.deployments.repositories import DeploymentArtifactRepository

class ArtifactService(BaseService):
    def __init__(self):
        super().__init__(repository=DeploymentArtifactRepository)

    def attach_artifact(self, deployment, s3_url, artifact_type):
        self._log_operation("attach_artifact", deployment_id=str(deployment.id), artifact_type=artifact_type)
        return self.repository.create(deployment_id=deployment.id, s3_url=s3_url, artifact_type=artifact_type)
