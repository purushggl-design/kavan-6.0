import pytest
from apps.deployments.models import Deployment, DeploymentState, DeploymentJob, DeploymentTemplate
from apps.deployments.services import StateMachineService, ProvisionService
from apps.tenants.models.tenant import Tenant
from apps.marketplace.models.product import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestDeploymentStateMachine:
    def setup_method(self):
        self.user = User.objects.create_user(email="deploy@example.com", password="pwd")
        self.tenant = Tenant.objects.create(tenant_code="deploy-corp", company_name="Deploy Corp", owner=self.user)
        self.product = Product.objects.create(name="Test Product", slug="test", code="test", status="PUBLISHED")
        self.template = DeploymentTemplate.objects.create(name="Test Template", product=self.product, docker_image="nginx:latest")
        self.deployment = Deployment.objects.create(
            tenant=self.tenant, 
            product=self.product,
            template_id=self.template.id,
            status=DeploymentState.REQUESTED
        )
        self.job = DeploymentJob.objects.create(deployment=self.deployment)

    def test_state_transition_valid(self):
        # Transition to QUEUED -> VALIDATING -> PROVISIONING
        StateMachineService.transition(self.deployment, DeploymentState.QUEUED, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.VALIDATING, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.PROVISIONING, self.job)
        self.deployment.refresh_from_db()
        assert self.deployment.status == DeploymentState.PROVISIONING
        
        # Test full provisioning pipeline
        StateMachineService.transition(self.deployment, DeploymentState.INSTALLING, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.CONFIGURING, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.STARTING, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.HEALTH_CHECK, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.RUNNING, self.job)
        self.deployment.refresh_from_db()
        assert self.deployment.status == DeploymentState.RUNNING

    def test_rollback_transition(self):
        # Simulate a failure
        StateMachineService.transition(self.deployment, DeploymentState.FAILED, self.job)
        self.deployment.refresh_from_db()
        assert self.deployment.status == DeploymentState.FAILED
        
        # Trigger Rollback
        StateMachineService.transition(self.deployment, DeploymentState.ROLLBACK, self.job)
        self.deployment.refresh_from_db()
        StateMachineService.transition(self.deployment, DeploymentState.ROLLED_BACK, self.job)
        self.deployment.refresh_from_db()
        assert self.deployment.status == DeploymentState.ROLLED_BACK
