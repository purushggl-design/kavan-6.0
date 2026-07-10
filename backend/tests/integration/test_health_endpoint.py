"""
KAVAN v6.0 — Integration Tests: Health Endpoints
"""

import pytest
from django.test import TestCase, Client
from unittest.mock import patch


@pytest.mark.integration
class TestHealthEndpoints(TestCase):
    """Integration tests for all /health/* endpoints."""

    def setUp(self):
        self.client = Client()

    # ----------------------------------------------------------
    # GET /health/live/
    # ----------------------------------------------------------

    def test_liveness_returns_200(self):
        """Liveness probe must return 200 when app is running."""
        response = self.client.get("/health/live/")
        self.assertEqual(response.status_code, 200)

    def test_liveness_response_format(self):
        """Liveness probe must return status=alive."""
        response = self.client.get("/health/live/")
        data = response.json()
        self.assertEqual(data["status"], "alive")
        self.assertIn("timestamp", data)
        self.assertIn("uptime_seconds", data)

    # ----------------------------------------------------------
    # GET /health/ready/
    # ----------------------------------------------------------

    @patch("monitoring.health_checks.check_database")
    @patch("monitoring.health_checks.check_redis")
    def test_readiness_returns_200_when_services_ok(self, mock_redis, mock_db):
        """Readiness probe returns 200 when DB and Redis are available."""
        mock_db.return_value = {"status": "ok", "latency_ms": 1.0, "message": "OK"}
        mock_redis.return_value = {"status": "ok", "latency_ms": 1.0, "message": "OK"}

        response = self.client.get("/health/ready/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ready")
        self.assertTrue(data["database"])
        self.assertTrue(data["redis"])

    @patch("apps.monitoring.health.views.check_database")
    @patch("apps.monitoring.health.views.check_redis")
    def test_readiness_returns_503_when_db_down(self, mock_redis, mock_db):
        """Readiness probe returns 503 when database is down."""
        mock_db.return_value = {"status": "error", "latency_ms": 0, "message": "Connection refused"}
        mock_redis.return_value = {"status": "ok", "latency_ms": 1.0, "message": "OK"}

        response = self.client.get("/health/ready/")
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data["status"], "not_ready")
        self.assertFalse(data["database"])

    # ----------------------------------------------------------
    # GET /health/
    # ----------------------------------------------------------

    @patch("apps.monitoring.health.views.check_database")
    @patch("apps.monitoring.health.views.check_redis")
    @patch("apps.monitoring.health.views.check_celery")
    def test_full_health_returns_200_when_all_ok(self, mock_celery, mock_redis, mock_db):
        """Full health check returns 200 when all services are OK."""
        ok = {"status": "ok", "latency_ms": 1.0, "message": "OK"}
        mock_db.return_value = ok
        mock_redis.return_value = ok
        mock_celery.return_value = ok

        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["status"], "healthy")

    @patch("apps.monitoring.health.views.check_database")
    @patch("apps.monitoring.health.views.check_redis")
    @patch("apps.monitoring.health.views.check_celery")
    def test_full_health_returns_503_when_db_down(self, mock_celery, mock_redis, mock_db):
        """Full health check returns 503 when database is down."""
        mock_db.return_value = {"status": "error", "latency_ms": 0, "message": "Error"}
        mock_redis.return_value = {"status": "ok", "latency_ms": 1.0, "message": "OK"}
        mock_celery.return_value = {"status": "ok", "latency_ms": 1.0, "message": "OK"}

        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["data"]["status"], "degraded")

    def test_health_response_has_request_id_header(self):
        """All health responses must include X-Request-ID header."""
        response = self.client.get("/health/live/")
        self.assertIn("X-Request-ID", response)

    def test_health_response_has_meta(self):
        """Full health response must include meta object."""
        response = self.client.get("/health/")
        data = response.json()
        self.assertIn("meta", data)
        self.assertIn("timestamp", data["meta"])
        self.assertIn("request_id", data["meta"])
        self.assertIn("version", data["meta"])

    # ----------------------------------------------------------
    # GET /health/db/
    # ----------------------------------------------------------

    @patch("monitoring.health_checks.check_database")
    def test_database_health_endpoint(self, mock_db):
        """Database health endpoint returns service-specific data."""
        mock_db.return_value = {"status": "ok", "latency_ms": 2.5, "message": "OK"}
        response = self.client.get("/health/db/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["service"], "database")
        self.assertEqual(data["status"], "ok")
