from rest_framework import serializers
from apps.tenants.models.tenant import Tenant
from apps.tenants.models.subscription import Subscription
from apps.tenants.models.tenant_settings import TenantSettings
from apps.tenants.models.deployment import Deployment
from apps.tenants.models.tenant_metrics import TenantMetrics
from apps.tenants.models.tenant_backup import TenantBackup

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class TenantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantSettings
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'

class TenantMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantMetrics
        fields = '__all__'

class TenantBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantBackup
        fields = '__all__'
