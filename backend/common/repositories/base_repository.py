"""
KAVAN v6.0 — Base Repository
============================================================
The Repository pattern abstracts database operations from
business logic. Services work with repositories, not directly
with Django ORM querysets.

Benefits:
  - Testable: swap with in-memory or mock repositories
  - Decoupled: services don't know about ORM internals
  - Consistent: single place for query logic
  - Extensible: add caching, logging, tenant filtering here

Usage:
    class UserRepository(BaseRepository):
        model = User

    repo = UserRepository()
    user = repo.get_by_id(user_id)
    users = repo.list(is_active=True)
"""

import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from config.exceptions.business import ResourceNotFoundException

logger = logging.getLogger("kavan")

# Generic type variable for model classes
ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing CRUD operations for any Django model.

    Subclasses must set the `model` class attribute.
    """

    model: Type[ModelType] = None

    def __init__(self):
        if self.model is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} must define a `model` class attribute."
            )

    # --------------------------------------------------------
    # READ operations
    # --------------------------------------------------------

    def get_by_id(self, pk: Any, raise_404: bool = True) -> Optional[ModelType]:
        """
        Retrieve a single record by primary key.

        Args:
            pk:        Primary key value (UUID or int)
            raise_404: If True, raise ResourceNotFoundException when not found

        Returns:
            Model instance or None
        """
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            if raise_404:
                raise ResourceNotFoundException(
                    resource_type=self.model.__name__,
                    resource_id=str(pk),
                )
            return None
        except Exception as exc:
            logger.error(
                f"Error fetching {self.model.__name__} by id={pk}: {exc}",
                exc_info=True,
            )
            raise

    def get_by_field(self, raise_404: bool = True, **kwargs) -> Optional[ModelType]:
        """
        Retrieve a single record by arbitrary field values.

        Args:
            raise_404: If True, raise ResourceNotFoundException when not found
            **kwargs:  Field name/value pairs for filtering

        Returns:
            Model instance or None
        """
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            if raise_404:
                raise ResourceNotFoundException(resource_type=self.model.__name__)
            return None
        except self.model.MultipleObjectsReturned:
            logger.warning(
                f"Multiple {self.model.__name__} objects returned for filter: {kwargs}"
            )
            return self.model.objects.filter(**kwargs).first()

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        active_only: bool = True,
    ):
        """
        Retrieve a filtered queryset.

        Args:
            filters:     Dict of field lookups (e.g. {"status": "active"})
            order_by:    List of field names to order by
            active_only: If True and model has is_active, filter to active only

        Returns:
            QuerySet
        """
        queryset = self.model.objects.all()

        # Apply soft delete filter if model supports it
        if active_only and hasattr(self.model, "is_active"):
            queryset = queryset.filter(is_active=True)

        # Apply additional filters
        if filters:
            queryset = queryset.filter(**filters)

        # Apply ordering
        if order_by:
            queryset = queryset.order_by(*order_by)

        return queryset

    def exists(self, **kwargs) -> bool:
        """Return True if any record matches the given field values."""
        return self.model.objects.filter(**kwargs).exists()

    def count(self, **kwargs) -> int:
        """Return the count of records matching the given field values."""
        return self.model.objects.filter(**kwargs).count()

    # --------------------------------------------------------
    # WRITE operations
    # --------------------------------------------------------

    def create(self, **kwargs) -> ModelType:
        """
        Create and return a new model instance.

        Args:
            **kwargs: Field name/value pairs

        Returns:
            Newly created model instance
        """
        instance = self.model.objects.create(**kwargs)
        logger.info(f"Created {self.model.__name__} id={instance.pk}")
        return instance

    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        Update fields on an existing model instance.

        Args:
            instance: The model instance to update
            **kwargs: Field name/value pairs to update

        Returns:
            Updated model instance
        """
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(kwargs.keys()) + ["updated_at"])
        logger.info(f"Updated {self.model.__name__} id={instance.pk}")
        return instance

    def delete(self, instance: ModelType) -> None:
        """
        Physically delete a model instance from the database.
        Prefer soft_delete() for domain models.
        """
        pk = instance.pk
        instance.delete()
        logger.info(f"Deleted {self.model.__name__} id={pk}")

    def soft_delete(self, instance: ModelType) -> ModelType:
        """
        Soft-delete a model instance by setting is_active=False.
        Requires SoftDeleteMixin.
        """
        if not hasattr(instance, "is_active"):
            raise AttributeError(
                f"{self.model.__name__} does not support soft delete. "
                "Ensure it uses SoftDeleteMixin."
            )
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        logger.info(f"Soft-deleted {self.model.__name__} id={instance.pk}")
        return instance

    def bulk_create(self, instances: List[ModelType]) -> List[ModelType]:
        """Bulk-create model instances for performance."""
        created = self.model.objects.bulk_create(instances)
        logger.info(f"Bulk created {len(created)} {self.model.__name__} records")
        return created
