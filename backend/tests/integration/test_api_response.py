"""
KAVAN v6.0 — Integration Tests: API Response Format
"""

import pytest
from django.test import TestCase, Client
from unittest.mock import patch


@pytest.mark.integration
class TestStandardResponseFormat(TestCase):
    """Tests that all API responses follow the KAVAN standard envelope."""

    def setUp(self):
        self.client = Client()

    def test_success_response_has_required_fields(self):
        """Success responses must have success, message, data, errors, meta."""
        response = self.client.get("/health/")
        data = response.json()

        required_fields = ["success", "message", "data", "errors", "meta"]
        for field in required_fields:
            self.assertIn(field, data, f"Missing field: {field}")

    def test_success_response_success_is_boolean(self):
        """success field must be a boolean."""
        response = self.client.get("/health/")
        data = response.json()
        self.assertIsInstance(data["success"], bool)

    def test_success_response_meta_has_required_fields(self):
        """meta object must have timestamp, request_id, version."""
        response = self.client.get("/health/")
        meta = response.json()["meta"]

        self.assertIn("timestamp", meta)
        self.assertIn("request_id", meta)
        self.assertIn("version", meta)

    def test_meta_version_is_v1(self):
        """API version in meta must be v1."""
        response = self.client.get("/health/")
        meta = response.json()["meta"]
        self.assertEqual(meta["version"], "v1")

    def test_meta_timestamp_is_iso_format(self):
        """Timestamp in meta must be ISO 8601 format."""
        from datetime import datetime
        response = self.client.get("/health/")
        meta = response.json()["meta"]
        timestamp = meta["timestamp"]
        # Should parse without error
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            self.fail(f"Timestamp {timestamp!r} is not valid ISO format")

    def test_content_type_is_json(self):
        """All API responses must have application/json content type."""
        response = self.client.get("/health/")
        self.assertIn("application/json", response.get("Content-Type", ""))
