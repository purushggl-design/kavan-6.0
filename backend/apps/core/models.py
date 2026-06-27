"""
KAVAN v6.0 — Core App Models
============================================================
The core app re-exports BaseModel from common for convenience
and defines infrastructure-level models (not domain models).

Domain models (User, Tenant, Product, etc.) live in their
respective app modules (Layer 2+).
"""

from common.models.base_model import BaseModel
from common.models.mixins import (
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    ActiveManager,
    AuditMixin,
    TenantMixin,
)

__all__ = [
    "BaseModel",
    "UUIDMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "ActiveManager",
    "AuditMixin",
    "TenantMixin",
]
