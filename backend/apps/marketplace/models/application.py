from django.db import models
from django.core.exceptions import ValidationError
from common.models.base_model import BaseModel
from apps.tenants.models.tenant import Tenant

class ApplicationStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    DEPRECATED = 'DEPRECATED', 'Deprecated'

class Application(BaseModel):
    """
    Represents a tenant-agnostic marketplace application.
    """
    code = models.CharField(max_length=100, unique=True, help_text='Unique identifier, e.g., gitlab, redis')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)

    class Meta:
        db_table = 'marketplace_applications'

    def __str__(self):
        return self.name

def validate_manifest(manifest):
    """
    Validates that the manifest JSON contains required keys for provisioning.
    Required: runtime.container_port, runtime.health_check_path, resources, env_schema
    """
    if not isinstance(manifest, dict):
        raise ValidationError("Manifest must be a JSON object.")
        
    required_top_level = ['runtime', 'resources', 'env_schema']
    for key in required_top_level:
        if key not in manifest:
            raise ValidationError(f"Manifest missing required key: '{key}'")
            
    runtime = manifest.get('runtime', {})
    if not isinstance(runtime, dict):
        raise ValidationError("'runtime' must be an object.")
        
    if 'container_port' not in runtime:
        raise ValidationError("Manifest missing 'runtime.container_port'.")
    if 'health_check_path' not in runtime:
        raise ValidationError("Manifest missing 'runtime.health_check_path'.")

class ApplicationVersion(BaseModel):
    """
    Represents a specific version/image of an application.
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50, help_text='e.g., 1.0.0')
    image_ref = models.CharField(max_length=255, help_text='e.g., localhost:5000/myapp:v1')
    manifest = models.JSONField(
        default=dict, 
        validators=[validate_manifest],
        help_text='JSON schema defining env_schema, runtime, resources'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'marketplace_application_versions'
        unique_together = ('application', 'version_number')

    def __str__(self):
        return f"{self.application.name} - {self.version_number}"

class InstallationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RUNNING = 'RUNNING', 'Running'
    FAILED = 'FAILED', 'Failed'
    STOPPED = 'STOPPED', 'Stopped'

class TenantInstallation(BaseModel):
    """
    Represents an actual running instance of an application for a specific tenant.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='installations')
    version = models.ForeignKey(ApplicationVersion, on_delete=models.RESTRICT, related_name='installations')
    status = models.CharField(max_length=32, choices=InstallationStatus.choices, default=InstallationStatus.PENDING)
    route_path = models.CharField(max_length=255, blank=True, help_text='Traefik routing path e.g., /tenant-a/app')
    config_overrides = models.JSONField(default=dict, blank=True, help_text='Tenant specific environment values')

    class Meta:
        db_table = 'marketplace_tenant_installations'
        
    def __str__(self):
        return f"{self.tenant.name} - {self.version.application.name} ({self.status})"
