"""
KAVAN v6.0 — Permission Constants (Layer 4 RBAC Placeholder)
"""

from enum import unique, StrEnum


@unique
class Permission(StrEnum):
    """
    Fine-grained permission constants.
    Format: resource:action
    """

    # --------------------------------------------------------
    # User Permissions (Layer 2)
    # --------------------------------------------------------
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_LIST = "user:list"

    # --------------------------------------------------------
    # Tenant Permissions (Layer 3)
    # --------------------------------------------------------
    TENANT_CREATE = "tenant:create"
    TENANT_READ = "tenant:read"
    TENANT_UPDATE = "tenant:update"
    TENANT_DELETE = "tenant:delete"
    TENANT_MANAGE = "tenant:manage"

    # --------------------------------------------------------
    # Role/Permission Management (Layer 4)
    # --------------------------------------------------------
    ROLE_ASSIGN = "role:assign"
    ROLE_REVOKE = "role:revoke"
    PERMISSION_MANAGE = "permission:manage"

    # --------------------------------------------------------
    # Product Permissions (Layer 5+)
    # --------------------------------------------------------
    PRODUCT_CREATE = "product:create"
    PRODUCT_READ = "product:read"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"
    PRODUCT_PUBLISH = "product:publish"

    # --------------------------------------------------------
    # Admin
    # --------------------------------------------------------
    ADMIN_ACCESS = "admin:access"
    AUDIT_LOG_READ = "audit:read"
    SYSTEM_SETTINGS_MANAGE = "system:manage"
