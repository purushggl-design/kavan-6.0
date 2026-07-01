# Layer 5 — Marketplace Permissions
# These constants align with Layer 4 RBAC rules

PLATFORM_PERMISSIONS = [
    "product:create",
    "product:update",
    "product:delete",
    "product:publish",
    "product:archive",
    "product:feature",
    "product:restore",
    "version:create",
    "version:update",
    "version:delete",
    "analytics:view",
    "category:create",
    "dependency:update",
]

TENANT_PERMISSIONS = [
    "marketplace:view",
    "marketplace:subscribe",
    "marketplace:unsubscribe",
    "product:view",
    "product:update",
    "product:configure",
    "product:deploy",
    "product:update_version",
]

# When Layer 4 RBAC is fully active, these will be checked via decorators or middleware
