"""
KAVAN v6.0 — Base Model
============================================================
All domain models extend BaseModel, which provides:
  - id:         UUID4 primary key (not sequential integers)
  - created_at: Auto-set timestamp when record is created
  - updated_at: Auto-updated timestamp on every save
  - is_active:  Soft delete flag (False = logically deleted)

Why UUID instead of integer:
  - Security: IDs are not guessable/enumerable
  - Distribution: Safe for distributed systems
  - Multi-tenancy: No ID conflicts across shards

Why soft delete:
  - Audit trail: Records are never physically deleted
  - Data recovery: Accidental deletes are recoverable
  - Foreign keys: No cascade delete complexity
"""

import uuid

from django.db import models

from common.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class BaseModel(UUIDMixin, TimestampMixin, SoftDeleteMixin, models.Model):
    """
    Abstract base model for all KAVAN domain models.

    Provides UUID PK, timestamps, and soft delete out of the box.
    All concrete models should extend this class.

    Usage:
        class MyModel(BaseModel):
            name = models.CharField(max_length=255)

            class Meta(BaseModel.Meta):
                db_table = "my_model"
    """

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def soft_delete(self) -> None:
        """Mark the record as inactive (soft delete)."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    @property
    def is_deleted(self) -> bool:
        """Return True if this record has been soft-deleted."""
        return not self.is_active
