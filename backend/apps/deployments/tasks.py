from celery import shared_task
from apps.deployments.models import Deployment, DeploymentJob
from apps.deployments.services.deployment_service import StateMachineService
from apps.deployments.services.provision_service import ProvisionService
from apps.deployments.services.rollback_service import RollbackService
from apps.deployments.services.upgrade_service import UpgradeService
from apps.deployments.services.health_service import HealthService
from apps.deployments.providers.docker_provider import DockerProvider

@shared_task(bind=True, max_retries=3)
def deploy_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    provider = DockerProvider()
    try:
        service = ProvisionService(provider=provider)
        service.provision(deployment, job)
    except Exception as exc:
        StateMachineService().transition(deployment, 'FAILED', job)
        rollback_product_task.delay(deployment_id, job_id)
        self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def rollback_product_task(self, deployment_id, job_id):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.filter(id=job_id).first()
    provider = DockerProvider()
    service = RollbackService(provider=provider)
    service.rollback(deployment, job)

@shared_task
def restart_product_task(deployment_id):
    deployment = Deployment.objects.get(id=deployment_id)
    provider = DockerProvider()
    provider.restart_infrastructure(deployment)

@shared_task
def upgrade_product_task(deployment_id, job_id, new_version_tag):
    deployment = Deployment.objects.get(id=deployment_id)
    job = DeploymentJob.objects.get(id=job_id)
    UpgradeService().upgrade(deployment, job, new_version_tag)

@shared_task
def health_check_task():
    provider = DockerProvider()
    service = HealthService(provider=provider)
    for deployment in Deployment.objects.filter(status='RUNNING'):
        is_healthy = service.check_health(deployment)
        # Handle unhealthy status based on requirements

@shared_task
def cleanup_failed_task():
    pass

@shared_task
def deployment_timeout_task():
    pass

import docker
import secrets
from apps.marketplace.models.application import TenantInstallation

@shared_task(bind=True, max_retries=1)
def provision_tenant_service(self, installation_id):
    try:
        installation = TenantInstallation.objects.get(id=installation_id)
    except TenantInstallation.DoesNotExist:
        return
        
    try:
        manifest = installation.version.manifest
        env_schema = manifest.get('env_schema', {})
        runtime = manifest.get('runtime', {})
        resources = manifest.get('resources', {})
        
        # Build environment
        env = {}
        for key in env_schema.get('kavan_generated', []):
            env[key] = secrets.token_urlsafe(32)
            
        for key in env_schema.get('kavan_provisioned', []):
            # TODO: Call provision_tenant_resource() here when built
            env[key] = "stubbed_provisioned_value"
            
        client = docker.from_env()
        
        container_name = f"kavan_tenant_{installation.tenant.tenant_code}_{installation.version.application.code}"
        
        # Remove stale container
        try:
            old_container = client.containers.get(container_name)
            old_container.remove(force=True)
        except docker.errors.NotFound:
            pass
            
        # Traefik labels
        route_path = f"/t/{installation.tenant.tenant_code}/{installation.version.application.code}"
        labels = {
            "traefik.enable": "true",
            f"traefik.http.routers.{container_name}.rule": f"PathPrefix(`{route_path}`)",
            f"traefik.http.services.{container_name}.loadbalancer.server.port": str(runtime.get('container_port', 80))
        }
        
        # Resource limits
        mem_limit = resources.get('mem_limit', None)
        nano_cpus = int(float(resources.get('cpu_limit', 0)) * 1e9) if 'cpu_limit' in resources else None
        
        # Spin up container
        container = client.containers.run(
            installation.version.image_ref,
            name=container_name,
            environment=env,
            network="kavan_default",
            labels=labels,
            mem_limit=mem_limit,
            nano_cpus=nano_cpus,
            detach=True
        )
        
        installation.status = 'RUNNING'
        installation.route_path = route_path
        installation.save()
        
    except Exception as exc:
        installation.status = 'FAILED'
        installation.save()
        self.retry(exc=exc, countdown=5)

