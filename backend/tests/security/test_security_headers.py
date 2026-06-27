"""
KAVAN v6.0 — Security Tests: HTTP Security Headers
"""

import pytest
from django.test import TestCase, Client, override_settings


@pytest.mark.security
class TestSecurityHeaders(TestCase):
    """Tests that security headers are present and correct."""

    def setUp(self):
        self.client = Client()
        self.response = self.client.get("/health/live/")

    def test_x_content_type_options_header(self):
        """X-Content-Type-Options must be nosniff."""
        self.assertEqual(
            self.response.get("X-Content-Type-Options"),
            "nosniff",
        )

    def test_x_frame_options_header(self):
        """X-Frame-Options must be DENY."""
        self.assertEqual(
            self.response.get("X-Frame-Options"),
            "DENY",
        )

    def test_x_xss_protection_header(self):
        """X-XSS-Protection must be 1; mode=block."""
        self.assertEqual(
            self.response.get("X-XSS-Protection"),
            "1; mode=block",
        )

    def test_referrer_policy_header(self):
        """Referrer-Policy must be set."""
        referrer_policy = self.response.get("Referrer-Policy")
        self.assertIsNotNone(referrer_policy)
        self.assertEqual(referrer_policy, "strict-origin-when-cross-origin")

    def test_permissions_policy_header(self):
        """Permissions-Policy must be set."""
        permissions_policy = self.response.get("Permissions-Policy")
        self.assertIsNotNone(permissions_policy)
        self.assertIn("camera=()", permissions_policy)
        self.assertIn("microphone=()", permissions_policy)

    def test_content_security_policy_header(self):
        """Content-Security-Policy header must be set."""
        csp = self.response.get("Content-Security-Policy")
        self.assertIsNotNone(csp)
        self.assertIn("default-src", csp)

    def test_x_request_id_header_present(self):
        """X-Request-ID must be present in all responses."""
        request_id = self.response.get("X-Request-ID")
        self.assertIsNotNone(request_id)
        # Should be a valid UUID
        import uuid
        try:
            uuid.UUID(request_id)
        except ValueError:
            self.fail(f"X-Request-ID {request_id!r} is not a valid UUID")

    def test_no_server_header_exposed(self):
        """Server header should not expose Django/Python version."""
        server = self.response.get("Server", "")
        self.assertNotIn("Django", server)
        self.assertNotIn("Python", server)

    @override_settings(DEBUG=False, SECURE_HSTS_SECONDS=31536000)
    def test_hsts_header_in_production(self):
        """HSTS header must be present in production mode."""
        # Re-instantiate middleware with DEBUG=False
        from django.test import RequestFactory
        from config.middleware.security import SecurityHeadersMiddleware

        factory = RequestFactory()
        request = factory.get("/health/live/")

        from django.http import HttpResponse
        middleware = SecurityHeadersMiddleware(lambda r: HttpResponse())
        response = middleware(request)

        hsts = response.get("Strict-Transport-Security")
        self.assertIsNotNone(hsts)
        self.assertIn("max-age=", hsts)

    def test_cache_control_header(self):
        """Cache-Control must prevent caching of API responses."""
        cache_control = self.response.get("Cache-Control", "")
        self.assertIn("no-store", cache_control)
