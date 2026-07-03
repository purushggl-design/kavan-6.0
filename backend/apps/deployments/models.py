import uuid
from django.db import models
from common.models.mixins import TimestampMixin
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

class DeploymentTemplate(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deployment_templates', null=True, blank=True)
    docker_image = models.CharField(max_length=512)
    helm_chart = models.CharField(max_length=512, blank=True)
    
    class Meta:
        db_table = 'deployments_template'

class DeploymentEnvironment(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100) # e.g. dev, staging, prod
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='environments')
    
    class Meta:
        db_table = 'deployments_environment'

class Deployment(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='deployments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deployments')
    environment = models.ForeignKey(DeploymentEnvironment, on_delete=models.SET_NULL, null=True, blank=True)
    template = models.ForeignKey(DeploymentTemplate, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, choices=DeploymentState.choices, default=DeploymentState.REQUESTED)
    version_tag = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'deployments_deployment'

class DeploymentJob(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='jobs')
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=DeploymentState.choices, default=DeploymentState.QUEUED)
    
    class Meta:
        db_table = 'deployments_job'

class DeploymentHistory(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'deployments_history'

class DeploymentLog(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(DeploymentJob, on_delete=models.CASCADE, related_name='logs')
    log_output = models.TextField()
    
    class Meta:
        db_table = 'deployments_log'

class DeploymentArtifact(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='artifacts')
    s3_url = models.URLField(max_length=1024)
    artifact_type = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'deployments_artifact'

class DeploymentVariable(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='variables')
    key = models.CharField(max_length=255)
    value = models.TextField()
    
    class Meta:
        db_table = 'deployments_variable'

class DeploymentSecret(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='secrets')
    key = models.CharField(max_length=255)
    vault_path = models.CharField(max_length=1024, help_text="Path in HashiCorp Vault or similar")
    
    class Meta:
        db_table = 'deployments_secret'

class DeploymentHealth(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='health_checks')
    is_healthy = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)
    metrics = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'deployments_health'

class DeploymentEvent(TimestampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'deployments_event'
