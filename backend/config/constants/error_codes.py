"""
KAVAN v6.0 — Error Code Constants
============================================================
Machine-readable error codes used in API error responses.
These codes allow frontend clients to handle errors programmatically.

Convention: SCREAMING_SNAKE_CASE
"""

from enum import unique, StrEnum


@unique
class ErrorCode(StrEnum):
    """All application error codes."""

    # --------------------------------------------------------
    # Generic
    # --------------------------------------------------------
    INTERNAL_ERROR = "INTERNAL_ERROR"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    BAD_REQUEST = "BAD_REQUEST"

    # --------------------------------------------------------
    # Authentication (Layer 2)
    # --------------------------------------------------------
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"

    # --------------------------------------------------------
    # Authorization / Permissions (Layer 4)
    # --------------------------------------------------------
    PERMISSION_DENIED = "PERMISSION_DENIED"
    OPERATION_NOT_PERMITTED = "OPERATION_NOT_PERMITTED"

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FIELD_VALIDATION_ERROR = "FIELD_VALIDATION_ERROR"
    REQUIRED_FIELD = "REQUIRED_FIELD"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    DUPLICATE_VALUE = "DUPLICATE_VALUE"

    # --------------------------------------------------------
    # Resources
    # --------------------------------------------------------
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    CONFLICT = "CONFLICT"

    # --------------------------------------------------------
    # Rate Limiting
    # --------------------------------------------------------
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"

    # --------------------------------------------------------
    # Tenancy (Layer 3)
    # --------------------------------------------------------
    TENANT_NOT_FOUND = "TENANT_NOT_FOUND"
    TENANT_SUSPENDED = "TENANT_SUSPENDED"
    TENANT_QUOTA_EXCEEDED = "TENANT_QUOTA_EXCEEDED"

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------
    HEALTH_CHECK_FAILED = "HEALTH_CHECK_FAILED"
    DATABASE_UNAVAILABLE = "DATABASE_UNAVAILABLE"
    CACHE_UNAVAILABLE = "CACHE_UNAVAILABLE"
    BROKER_UNAVAILABLE = "BROKER_UNAVAILABLE"
