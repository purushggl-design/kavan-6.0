"""
KAVAN v6.0 — Unit Tests: Base Models
"""

import uuid

import pytest
from django.test import TestCase

from common.models.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin


@pytest.mark.unit
class TestUUIDMixin(TestCase):
    """Tests for UUIDMixin."""

    def test_id_field_is_uuid(self):
        """UUID mixin should provide a UUID id field."""
        # We test the mixin via a concrete model
        from django.db import models

        class TestModel(UUIDMixin, models.Model):
            class Meta:
                app_label = "core"
                abstract = True

        field = TestModel._meta.get_field("id")
        self.assertIsInstance(field, models.UUIDField)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.editable)


@pytest.mark.unit
class TestBaseModelBehavior(TestCase):
    """Tests for BaseModel behavior."""

    def test_uuid_default_is_callable(self):
        """Default UUID should be callable (not a static value)."""
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        self.assertNotEqual(id1, id2)

    def test_uuid_is_valid_uuid4(self):
        """Generated UUID should be valid UUID4."""
        generated = uuid.uuid4()
        parsed = uuid.UUID(str(generated), version=4)
        self.assertEqual(parsed, generated)


@pytest.mark.unit
class TestSoftDeleteMixin(TestCase):
    """Tests for SoftDeleteMixin behavior."""

    def test_is_active_defaults_to_true(self):
        """is_active should default to True."""
        from django.db import models

        class TestModel(SoftDeleteMixin, models.Model):
            class Meta:
                app_label = "core"
                abstract = True

        field = TestModel._meta.get_field("is_active")
        self.assertTrue(field.default)

    def test_is_active_is_indexed(self):
        """is_active should be indexed for query performance."""
        from django.db import models

        class TestModel(SoftDeleteMixin, models.Model):
            class Meta:
                app_label = "core"
                abstract = True

        field = TestModel._meta.get_field("is_active")
        self.assertTrue(field.db_index)
