import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from apps.marketplace.models.application import Application, ApplicationVersion, TenantInstallation, InstallationStatus
from apps.tenants.models.tenant import Tenant
from apps.monitoring.tasks import check_installation_health
from apps.audit.models import AuditEvent, AuditEventType

def verify():
    print("Setting up health monitoring test data...")
    owner_user, _ = User.objects.get_or_create(username="tenant_owner", defaults={"email": "owner@test.com", "platform_role": "TENANT_ADMIN"})
    tenant_c, _ = Tenant.objects.get_or_create(tenant_code="tenant_c", defaults={"tenant_name": "Tenant C", "owner": owner_user, "company_domain": "c.com"})

    app, _ = Application.objects.get_or_create(code="health-test", defaults={"name": "Health App", "description": "Test"})
    version, _ = ApplicationVersion.objects.get_or_create(
        application=app, 
        version_number="1.0.0", 
        defaults={
            "image_ref": "test:latest", 
            "is_active": True,
            "manifest": {
                "runtime": {
                    "container_port": 12345, # A port that definitely isn't listening (connection refused)
                    "health_check_path": "/healthz"
                },
                "resources": {},
                "env_schema": {}
            }
        }
    )

    TenantInstallation.objects.filter(tenant=tenant_c).delete()
    
    install = TenantInstallation.objects.create(
        tenant=tenant_c, 
        version=version, 
        status=InstallationStatus.RUNNING, 
        route_path="/t/tenant_c/health-test"
    )
    
    initial_updated_at = install.updated_at
    print(f"Created installation {install.id}, initial status: {install.status}")
    
    print("\n--- Running check_installation_health task synchronously ---")
    check_installation_health()
    
    install.refresh_from_db()
    
    print(f"Final status: {install.status}")
    print(f"Updated at changed: {install.updated_at != initial_updated_at}")
    
    assert install.status == InstallationStatus.FAILED, f"Expected FAILED, got {install.status}"
    
    audit_logs = AuditEvent.objects.filter(tenant_id=install.tenant.id, event_type=AuditEventType.INSTALLATION_FAILED)
    print(f"Audit logs generated: {audit_logs.count()}")
    for log in audit_logs:
        print(f"- Audit Log: {log.event_type} | {log.metadata}")
        
    assert audit_logs.exists(), "No audit log was generated for the health failure!"

    print("\nSUCCESS: Health check failed gracefully, updated status, and generated audit log.")

if __name__ == '__main__':
    verify()
