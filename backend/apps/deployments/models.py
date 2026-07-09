import uuid
from django.db import models
from common.models.base_model import BaseModel
from apps.tenants.models.tenant import Tenant
from apps.marketplace.models.product import Product

class DeploymentState(models.TextChoices):
    REQUESTED = 'REQUESTED', 'Requested'
    QUEUED = 'QUEUED', 'Queued'
    VALIDATING = 'VALIDATING', 'Validating'
    PROVISIONING = 'PROVISIONING', 'Provisioning'
    INSTALLING = 'INSTALLING', 'Installing'
    CONFIGURING = 'CONFIGURING', 'Configuring'
    STARTING = 'STARTING', 'Starting'
    HEALTH_CHECK = 'HEALTH_CHECK', 'Health Check'
    RUNNING = 'RUNNING', 'Running'
    FAILED = 'FAILED', 'Failed'
    ROLLBACK = 'ROLLBACK', 'Rollback'
    ROLLED_BACK = 'ROLLED_BACK', 'Rolled Back'

class DeploymentTemplate(BaseModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deployment_templates', null=True, blank=True)
    docker_image = models.CharField(max_length=512)
    helm_chart = models.CharField(max_length=512, blank=True)
    
    class Meta:
        db_table = 'deployments_template'

class DeploymentEnvironment(BaseModel):
    name = models.CharField(max_length=100) # e.g. dev, staging, prod
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='environments')
    
    class Meta:
        db_table = 'deployments_environment'

class Deployment(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='deployments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deployments')
    tenant_product = models.ForeignKey('marketplace.TenantProduct', on_delete=models.CASCADE, related_name='layer6_deployments', null=True)
    environment = models.ForeignKey(DeploymentEnvironment, on_delete=models.SET_NULL, null=True, blank=True)
    template = models.ForeignKey(DeploymentTemplate, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=DeploymentState.choices, default=DeploymentState.REQUESTED)
    version_tag = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'deployments_deployment'

class DeploymentJob(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='jobs')
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=DeploymentState.choices, default=DeploymentState.QUEUED)
    
    class Meta:
        db_table = 'deployments_job'

class DeploymentHistory(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'deployments_history'

class DeploymentLog(BaseModel):
    job = models.ForeignKey(DeploymentJob, on_delete=models.CASCADE, related_name='logs')
    log_output = models.TextField()
    
    class Meta:
        db_table = 'deployments_log'

class DeploymentArtifact(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='artifacts')
    s3_url = models.URLField(max_length=1024)
    artifact_type = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'deployments_artifact'

class DeploymentVariable(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='variables')
    key = models.CharField(max_length=255)
    value = models.TextField()
    
    class Meta:
        db_table = 'deployments_variable'

class DeploymentSecret(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='secrets')
    key = models.CharField(max_length=255)
    vault_path = models.CharField(max_length=1024, blank=True, help_text="Path in HashiCorp Vault or similar")
    value_encrypted = models.TextField(blank=True, help_text="Encrypted secret value if stored directly")
    
    class Meta:
        db_table = 'deployments_secret'

    def get_secret_value(self):
        if self.vault_path:
            return None
        if not self.value_encrypted:
            return None
            
        from apps.deployments.security.secret_backend import get_secret_backend
        backend = get_secret_backend()
        return backend.decrypt(self.value_encrypted)

    def set_secret_value(self, raw_value):
        from apps.deployments.security.secret_backend import get_secret_backend
        backend = get_secret_backend()
        self.value_encrypted = backend.encrypt(raw_value)

class DeploymentHealth(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='health_checks')
    is_healthy = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)
    metrics = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'deployments_health'

class DeploymentEvent(BaseModel):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'deployments_event'
