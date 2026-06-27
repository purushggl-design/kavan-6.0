"""
KAVAN v6.0 — Model Mixins
============================================================
Reusable model mixins following the Single Responsibility principle.
Compose mixins to add specific functionality to any model.
"""

import uuid

from django.db import models


class UUIDMixin(models.Model):
    """
    Adds a UUID4 primary key field.

    Using UUID instead of sequential integer prevents:
    - ID enumeration attacks
    - Conflicts in distributed environments
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Unique identifier (UUID4)",
    )

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    Adds auto-managed created_at and updated_at timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when this record was first created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Timestamp when this record was last modified.",
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Adds is_active flag for soft delete.

    Records are NEVER physically deleted — set is_active=False
    to logically remove them from normal queries.

    Use ActiveManager or filter(is_active=True) to exclude deleted records.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Is Active",
        help_text="False means this record has been soft-deleted.",
    )

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """
    Custom manager that returns only active (non-soft-deleted) records.

    Usage:
        class MyModel(BaseModel):
            objects = ActiveManager()
            all_objects = models.Manager()  # includes soft-deleted
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AuditMixin(models.Model):
    """
    Adds created_by and updated_by fields (Layer 2 — requires User model).
    This mixin is a placeholder; it becomes fully functional in Layer 2.
    """

    created_by = models.UUIDField(
        null=True,
        blank=True,
        verbose_name="Created By",
        help_text="UUID of the user who created this record.",
    )
    updated_by = models.UUIDField(
        null=True,
        blank=True,
        verbose_name="Updated By",
        help_text="UUID of the user who last updated this record.",
    )

    class Meta:
        abstract = True


class TenantMixin(models.Model):
    """
    Adds tenant_id for multi-tenancy isolation (Layer 3).
    This mixin is a placeholder; it becomes fully functional in Layer 3.
    """

    tenant_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Tenant ID",
        help_text="UUID of the tenant this record belongs to.",
    )

    class Meta:
        abstract = True
