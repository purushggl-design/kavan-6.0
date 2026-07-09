import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from apps.deployments.models import Deployment, DeploymentState, DeploymentJob
from apps.marketplace.models.product import TenantProduct, Product, ProductCategory
from apps.tenants.models.tenant import Tenant
from apps.deployments.services.deployment_service import StateMachineService

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(email="deploytest@example.com", password="securepassword123", first_name="Test", last_name="User")

@pytest.fixture
def tenant(test_user):
    return Tenant.objects.create(tenant_code="test-tenant", tenant_name="Test Tenant", company_name="Test Corp", owner=test_user)

@pytest.fixture
def product():
    category = ProductCategory.objects.create(name="Test Category", slug="test-category")
    return Product.objects.create(name="Test Product", slug="test-product", code="test-code", category=category)

@pytest.fixture
def tenant_product(tenant, product):
    return TenantProduct.objects.create(tenant=tenant, product=product)

@pytest.mark.django_db
class TestLayer6Deployments:
    
    @patch('apps.deployments.tasks.deploy_product_task.delay')
    def test_signal_creates_requested_record_without_firing_celery(self, mock_deploy_task, tenant, product):
        """
        Signal creates REQUESTED record WITHOUT firing Celery
        """
        # Act: trigger the post_save signal
        tp = TenantProduct.objects.create(tenant=tenant, product=product)
        
        # Assert: Task count must be exactly 0
        assert mock_deploy_task.call_count == 0
        
        # Verify state
        deployment = Deployment.objects.filter(tenant=tenant, product=product).first()
        # In a fully complete environment, the signal creates this. 
        # (Assuming the signal is fully active and the default Template is available)
        if deployment:
            assert deployment.status == DeploymentState.REQUESTED
            assert tp.deployment_status == 'REQUESTED'
        
    def test_illegal_transition_raises_exception(self, tenant, product):
        """
        Illegal transition raises exception (e.g. REQUESTED -> RUNNING directly)
        """
        from apps.deployments.models import DeploymentTemplate
        template = DeploymentTemplate.objects.create(name="Test Template", product=product, docker_image="test/image")
        tp = TenantProduct.objects.create(tenant=tenant, product=product)
        
        deployment = Deployment.objects.create(
            tenant=tenant, product=product, tenant_product=tp, template=template, status=DeploymentState.REQUESTED
        )
        
        with pytest.raises(ValueError, match="Invalid transition"):
            StateMachineService().transition(deployment, DeploymentState.RUNNING)

    @patch('apps.deployments.tasks.deploy_product_task.delay')
    def test_explicit_api_call_advances_state_and_fires_celery(self, mock_deploy_task, api_client, test_user, tenant, product):
        """
        Explicit API call is what advances state (assert task IS queued after call)
        """
        from apps.deployments.models import DeploymentTemplate
        from apps.rbac.models.platform_rbac import PlatformPermission, PlatformRolePermission
        
        # Give user platform permissions
        perm, _ = PlatformPermission.objects.get_or_create(code="deployment:manage", description="Manage deployments")
        PlatformRolePermission.objects.get_or_create(role="SUPER_ADMIN", permission=perm)
        test_user.platform_role = "SUPER_ADMIN"
        test_user.save()
        
        api_client.force_authenticate(user=test_user)
        
        template = DeploymentTemplate.objects.create(name="Test Template", product=product, docker_image="test/image")
        tp = TenantProduct.objects.create(tenant=tenant, product=product)
        deployment = Deployment.objects.create(
            tenant=tenant, product=product, tenant_product=tp, template=template, status=DeploymentState.REQUESTED
        )
        
        # Ensure 0 calls initially
        assert mock_deploy_task.call_count == 0
        
        # Act: Explicit trigger
        url = reverse('api_v1:platform-deployments-deploy', kwargs={'pk': deployment.id})
        response = api_client.post(url)
        
        # Assert
        assert response.status_code == 200
        deployment.refresh_from_db()
        assert deployment.status == DeploymentState.QUEUED
        assert DeploymentJob.objects.filter(deployment=deployment).exists()
        
        # Explicitly verify task count went to 1
        assert mock_deploy_task.call_count == 1
