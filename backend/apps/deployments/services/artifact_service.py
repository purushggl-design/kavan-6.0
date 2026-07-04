from apps.deployments.repositories import DeploymentArtifactRepository

class ArtifactService:
    @staticmethod
    def attach_artifact(deployment, s3_url, artifact_type):
        return DeploymentArtifactRepository.create(deployment.id, s3_url, artifact_type)
