import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.authentication.models import UserStatus
from apps.rbac.models.platform_rbac import PlatformPermission, PlatformRolePermission

User = get_user_model()


class Command(BaseCommand):
    help = 'Bootstraps the platform with default roles, permissions, categories, demo products, and SIEM rules.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting platform bootstrap..."))

        with transaction.atomic():
            self._bootstrap_permissions()
            self._bootstrap_admin()
            self._bootstrap_marketplace_categories()
            self._bootstrap_demo_products()
            self._bootstrap_siem_rules()

        self.stdout.write(self.style.SUCCESS("Platform bootstrap completed successfully!"))

    # ------------------------------------------------------------------
    # RBAC Permissions
    # ------------------------------------------------------------------
    def _bootstrap_permissions(self):
        permissions = [
            ("deployment:manage", "Manage Platform Deployments"),
            ("platform:create_tenant", "Create Tenants"),
            ("VIEW_METRICS", "View Platform Metrics"),
            ("VIEW_SECURITY_EVENTS", "View Security Events"),
            ("product:manage", "Manage Marketplace Products"),
            ("siem:view", "View SIEM Alerts and Rules"),
            ("incidents:manage", "Manage Incidents and Alerts"),
        ]

        for code, desc in permissions:
            perm, created = PlatformPermission.objects.get_or_create(
                code=code, defaults={"description": desc}
            )
            if created:
                self.stdout.write(f"  + Created permission: {code}")

            # Auto-assign all permissions to SUPER_ADMIN
            PlatformRolePermission.objects.get_or_create(
                role=User.PlatformRole.SUPER_ADMIN, permission=perm
            )

    # ------------------------------------------------------------------
    # Super Admin
    # ------------------------------------------------------------------
    def _bootstrap_admin(self):
        email = "admin@kavan.local"
        password = "Admin123!"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name="Platform",
                last_name="Admin",
                platform_role=User.PlatformRole.SUPER_ADMIN,
                status=UserStatus.ACTIVE,
                email_verified=True,
            )
            self.stdout.write(self.style.SUCCESS(f"  + Created Super Admin: {email} / {password}"))
        else:
            self.stdout.write(f"  ~ Super Admin already exists: {email}")

    # ------------------------------------------------------------------
    # Marketplace Categories
    # ------------------------------------------------------------------
    def _bootstrap_marketplace_categories(self):
        """Create default product categories for the marketplace."""
        try:
            from apps.marketplace.models.product import ProductCategory
        except ImportError:
            self.stdout.write(self.style.WARNING("  ! Marketplace app not available, skipping categories."))
            return

        categories = [
            ("Enterprise Resource Planning", "erp", "Full-suite ERP solutions for enterprise operations."),
            ("Customer Relationship Management", "crm", "CRM tools to manage customer interactions and pipelines."),
            ("HR Management", "hrms", "Human resource and workforce management solutions."),
            ("Help Desk & Support", "helpdesk", "Customer support and ticketing platforms."),
            ("Security & Compliance", "security", "Security tools, auditing, and compliance automation."),
            ("Analytics & BI", "analytics", "Business intelligence, reporting, and data analytics tools."),
        ]

        for name, slug, description in categories:
            _, created = ProductCategory.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": description}
            )
            if created:
                self.stdout.write(f"  + Created category: {name}")
            else:
                self.stdout.write(f"  ~ Category already exists: {name}")

    # ------------------------------------------------------------------
    # Demo Products
    # ------------------------------------------------------------------
    def _bootstrap_demo_products(self):
        """Create demo products in PUBLISHED state for marketplace browsing."""
        try:
            from apps.marketplace.models.product import (
                Product,
                ProductCategory,
                ProductVersion,
                MarketplaceListing,
                ProductStatus,
                ProductVisibility,
            )
        except ImportError:
            self.stdout.write(self.style.WARNING("  ! Marketplace app not available, skipping demo products."))
            return

        crm_cat = ProductCategory.objects.filter(slug="crm").first()
        hrms_cat = ProductCategory.objects.filter(slug="hrms").first()
        helpdesk_cat = ProductCategory.objects.filter(slug="helpdesk").first()

        demo_products = [
            {
                "code": "crm-pro",
                "name": "CRM Pro",
                "slug": "crm-pro",
                "short_description": "Enterprise CRM for sales, pipelines, and customer management.",
                "description": (
                    "CRM Pro is a full-featured customer relationship management system built for B2B enterprises. "
                    "Manage leads, contacts, deals, and pipelines from a single platform."
                ),
                "category": crm_cat,
                "vendor": "KAVAN Technologies",
                "status": ProductStatus.PUBLISHED,
                "visibility": ProductVisibility.PUBLIC,
                "license_type": "ENTERPRISE",
                "pricing_model": "SUBSCRIPTION",
                "version": "2.4.0",
            },
            {
                "code": "hrms-core",
                "name": "HRMS Core",
                "slug": "hrms-core",
                "short_description": "Modern HR management platform for workforce operations.",
                "description": (
                    "HRMS Core handles employee records, leave management, payroll integration, "
                    "onboarding workflows, and performance reviews in one unified platform."
                ),
                "category": hrms_cat,
                "vendor": "KAVAN Technologies",
                "status": ProductStatus.PUBLISHED,
                "visibility": ProductVisibility.PUBLIC,
                "license_type": "ENTERPRISE",
                "pricing_model": "SUBSCRIPTION",
                "version": "1.8.0",
            },
            {
                "code": "helpdesk-plus",
                "name": "Help Desk Plus",
                "slug": "helpdesk-plus",
                "short_description": "Multi-channel support ticket system with SLA management.",
                "description": (
                    "Help Desk Plus provides omni-channel ticketing, SLA tracking, knowledge base, "
                    "and team collaboration tools to deliver exceptional customer support."
                ),
                "category": helpdesk_cat,
                "vendor": "KAVAN Technologies",
                "status": ProductStatus.PUBLISHED,
                "visibility": ProductVisibility.PUBLIC,
                "license_type": "PROFESSIONAL",
                "pricing_model": "SUBSCRIPTION",
                "version": "3.1.0",
            },
        ]

        for product_data in demo_products:
            version_str = product_data.pop("version")
            product, created = Product.objects.get_or_create(
                code=product_data["code"], defaults=product_data
            )
            if created:
                self.stdout.write(f"  + Created product: {product.name}")
                ProductVersion.objects.create(
                    product=product,
                    version_number=version_str,
                    is_stable=True,
                    is_latest=True,
                    status="ACTIVE",
                )
                MarketplaceListing.objects.create(product=product)
            else:
                self.stdout.write(f"  ~ Product already exists: {product.name}")

    # ------------------------------------------------------------------
    # SIEM Detection Rules
    # ------------------------------------------------------------------
    def _bootstrap_siem_rules(self):
        """Create default SIEM detection rules."""
        try:
            from apps.siem.models.rules import DetectionRule, RuleType
            from apps.monitoring.models.events import EventSeverity
        except ImportError:
            self.stdout.write(self.style.WARNING("  ! SIEM app not available, skipping detection rules."))
            return

        rules = [
            {
                "name": "Brute Force Login Detection",
                "description": (
                    "Triggers when 5 or more failed login attempts occur within 5 minutes "
                    "for the same user/tenant."
                ),
                "rule_type": RuleType.THRESHOLD,
                "conditions": {"event_type": "FAILED_LOGIN"},
                "threshold": 5,
                "time_window_seconds": 300,
                "severity": EventSeverity.HIGH,
            },
            {
                "name": "Privilege Escalation Attempt",
                "description": (
                    "Triggers immediately when a user attempts an action beyond their RBAC permissions."
                ),
                "rule_type": RuleType.EXACT_MATCH,
                "conditions": {"event_type": "PERMISSION_DENIED", "action": "ESCALATION"},
                "threshold": 1,
                "time_window_seconds": 0,
                "severity": EventSeverity.CRITICAL,
            },
            {
                "name": "Mass Resource Deletion",
                "description": "Triggers when 10 or more DELETE actions are performed within 2 minutes.",
                "rule_type": RuleType.THRESHOLD,
                "conditions": {"action": "DELETE"},
                "threshold": 10,
                "time_window_seconds": 120,
                "severity": EventSeverity.HIGH,
            },
            {
                "name": "After-Hours Admin Access",
                "description": (
                    "Triggers when a platform admin logs in outside business hours. "
                    "Extend with time-of-day logic for production use."
                ),
                "rule_type": RuleType.EXACT_MATCH,
                "conditions": {"event_type": "LOGIN_SUCCESS", "action": "AFTER_HOURS"},
                "threshold": 1,
                "time_window_seconds": 0,
                "severity": EventSeverity.MEDIUM,
            },
        ]

        for rule_data in rules:
            _, created = DetectionRule.objects.get_or_create(
                name=rule_data["name"], defaults=rule_data
            )
            if created:
                self.stdout.write(f"  + Created SIEM rule: {rule_data['name']}")
            else:
                self.stdout.write(f"  ~ SIEM rule already exists: {rule_data['name']}")
