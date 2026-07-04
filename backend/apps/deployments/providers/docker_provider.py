import docker
from apps.deployments.providers.base import ProvisionProvider

class DockerProvider(ProvisionProvider):
    def provision_infrastructure(self, deployment):
        client = docker.from_env()
        image = deployment.template.docker_image
        if not image:
            raise ValueError("Docker image is required in deployment template")
            
        environment = {}
        for var in deployment.variables.all():
            environment[var.key] = var.value
            
        return client.containers.run(
            image=image,
            name=f"tenant-{deployment.tenant.id}-{deployment.product.slug}",
            detach=True,
            environment=environment,
            network="kavan_tenant_network",
        )

    def rollback_infrastructure(self, deployment):
        client = docker.from_env()
        name = f"tenant-{deployment.tenant.id}-{deployment.product.slug}"
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass

    def restart_infrastructure(self, deployment):
        client = docker.from_env()
        name = f"tenant-{deployment.tenant.id}-{deployment.product.slug}"
        try:
            container = client.containers.get(name)
            container.restart()
        except docker.errors.NotFound:
            pass

    def health_check(self, deployment):
        client = docker.from_env()
        name = f"tenant-{deployment.tenant.id}-{deployment.product.slug}"
        try:
            container = client.containers.get(name)
            container.reload()
            return container.status == 'running'
        except docker.errors.NotFound:
            return False
