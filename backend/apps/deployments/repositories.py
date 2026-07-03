from apps.deployments.models import (
    Deployment, DeploymentJob, DeploymentHistory, DeploymentLog, 
    DeploymentArtifact, DeploymentTemplate
)

class DeploymentRepository:
    @staticmethod
    def create(tenant, product, template, environment=None, status='REQUESTED'):
        return Deployment.objects.create(
            tenant=tenant, product=product, template=template,
            environment=environment, status=status
        )

    @staticmethod
    def update_status(deployment_id, new_status):
        Deployment.objects.filter(id=deployment_id).update(status=new_status)

class DeploymentJobRepository:
    @staticmethod
    def create(deployment_id, status='QUEUED'):
        return DeploymentJob.objects.create(deployment_id=deployment_id, status=status)
        
    @staticmethod
    def update_status(job_id, status):
        DeploymentJob.objects.filter(id=job_id).update(status=status)

class DeploymentHistoryRepository:
    @staticmethod
    def create(deployment_id, old_status, new_status):
        return DeploymentHistory.objects.create(
            deployment_id=deployment_id, old_status=old_status, new_status=new_status
        )

class DeploymentLogRepository:
    @staticmethod
    def append_log(job_id, log_output):
        return DeploymentLog.objects.create(job_id=job_id, log_output=log_output)

class DeploymentArtifactRepository:
    @staticmethod
    def create(deployment_id, s3_url, artifact_type):
        return DeploymentArtifact.objects.create(
            deployment_id=deployment_id, s3_url=s3_url, artifact_type=artifact_type
        )

class DeploymentTemplateRepository:
    @staticmethod
    def get_by_id(template_id):
        return DeploymentTemplate.objects.get(id=template_id)
