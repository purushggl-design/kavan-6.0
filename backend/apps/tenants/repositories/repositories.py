from common.repositories.base_repository import BaseRepository
from apps.tenants.models.tenant import Tenant
from apps.tenants.models.tenant_member import TenantMember
from apps.tenants.models.subscription import Subscription
from apps.tenants.models.tenant_settings import TenantSettings
from apps.tenants.models.deployment import Deployment
from apps.tenants.models.tenant_metrics import TenantMetrics
from apps.tenants.models.tenant_backup import TenantBackup

class TenantRepository(BaseRepository):
    model = Tenant

class TenantMemberRepository(BaseRepository):
    model = TenantMember

class SubscriptionRepository(BaseRepository):
    model = Subscription

class TenantSettingsRepository(BaseRepository):
    model = TenantSettings

class DeploymentRepository(BaseRepository):
    model = Deployment

class MetricsRepository(BaseRepository):
    model = TenantMetrics

class BackupRepository(BaseRepository):
    model = TenantBackup
