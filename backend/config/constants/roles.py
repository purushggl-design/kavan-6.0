"""
KAVAN v6.0 — Role Constants (Layer 4 RBAC Placeholder)
"""

from enum import unique, StrEnum


@unique
class Role(StrEnum):
    """System-defined roles."""

    # Platform-level roles
    SUPER_ADMIN = "super_admin"
    PLATFORM_ADMIN = "platform_admin"

    # Tenant-level roles (Layer 3)
    TENANT_OWNER = "tenant_owner"
    TENANT_ADMIN = "tenant_admin"
    TENANT_MANAGER = "tenant_manager"
    TENANT_MEMBER = "tenant_member"
    TENANT_VIEWER = "tenant_viewer"

    # Application roles (Layer 5+)
    PRODUCT_MANAGER = "product_manager"
    ANALYST = "analyst"
    SUPPORT = "support"
    GUEST = "guest"


# Human-readable role labels
ROLE_LABELS = {
    Role.SUPER_ADMIN: "Super Administrator",
    Role.PLATFORM_ADMIN: "Platform Administrator",
    Role.TENANT_OWNER: "Organization Owner",
    Role.TENANT_ADMIN: "Organization Administrator",
    Role.TENANT_MANAGER: "Organization Manager",
    Role.TENANT_MEMBER: "Organization Member",
    Role.TENANT_VIEWER: "Viewer",
    Role.PRODUCT_MANAGER: "Product Manager",
    Role.ANALYST: "Analyst",
    Role.SUPPORT: "Support Agent",
    Role.GUEST: "Guest",
}
