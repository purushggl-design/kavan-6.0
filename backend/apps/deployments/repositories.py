from common.repositories.base_repository import BaseRepository
from apps.deployments.models import (
    Deployment, DeploymentJob, DeploymentHistory, DeploymentLog, 
    DeploymentArtifact, DeploymentTemplate
)

class DeploymentRepository(BaseRepository):
    model = Deployment
    
    @classmethod
    def get_by_tenant_and_product(cls, tenant_id, product_id):
        return cls.get_queryset().filter(tenant_id=tenant_id, product_id=product_id)

    @classmethod
    def update_status(cls, deployment_id, new_status):
        cls.get_queryset().filter(id=deployment_id).update(status=new_status)

class DeploymentJobRepository(BaseRepository):
    model = DeploymentJob

    @classmethod
    def update_status(cls, job_id, status):
        cls.get_queryset().filter(id=job_id).update(status=status)

class DeploymentHistoryRepository(BaseRepository):
    model = DeploymentHistory

class DeploymentLogRepository(BaseRepository):
    model = DeploymentLog

    @classmethod
    def append_log(cls, job_id, log_output):
        return cls.create(job_id=job_id, log_output=log_output)

class DeploymentArtifactRepository(BaseRepository):
    model = DeploymentArtifact

class DeploymentTemplateRepository(BaseRepository):
    model = DeploymentTemplate
