"""
KAVAN v6.0 — Security Headers Middleware
============================================================
Injects HTTP security headers into every response.
These complement Django's built-in SecurityMiddleware.

Headers applied:
  - Strict-Transport-Security (HSTS)
  - X-Content-Type-Options
  - X-Frame-Options
  - X-XSS-Protection
  - Content-Security-Policy
  - Referrer-Policy
  - Permissions-Policy

Note: HSTS is only injected when DEBUG=False to avoid
      accidentally locking out local development.
"""

from django.conf import settings


class SecurityHeadersMiddleware:
    """
    Adds comprehensive security headers to all HTTP responses.

    Complements Django's SecurityMiddleware by providing
    additional headers not covered by the built-in implementation.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._debug = getattr(settings, "DEBUG", True)

    def __call__(self, request):
        response = self.get_response(request)
        self._apply_security_headers(response)
        return response

    def _apply_security_headers(self, response) -> None:
        """Apply all security headers to the response."""

        # Prevent MIME type sniffing
        response["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response["X-Frame-Options"] = "DENY"

        # Legacy XSS protection (for older browsers)
        response["X-XSS-Protection"] = "1; mode=block"

        # Referrer policy — limit referrer information leakage
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions policy — restrict browser features
        response["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), "
            "payment=(), usb=(), magnetometer=()"
        )

        # Content Security Policy
        # In production, tighten this per your frontend requirements
        if self._debug:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; "
                "font-src 'self' data:; "
                "connect-src 'self';"
            )
        else:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self'; "
                "img-src 'self' data:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )

        # HSTS — only in production (not over HTTP in development)
        if not self._debug:
            hsts_seconds = getattr(settings, "SECURE_HSTS_SECONDS", 31536000)
            hsts_value = f"max-age={hsts_seconds}"
            if getattr(settings, "SECURE_HSTS_INCLUDE_SUBDOMAINS", True):
                hsts_value += "; includeSubDomains"
            if getattr(settings, "SECURE_HSTS_PRELOAD", True):
                hsts_value += "; preload"
            response["Strict-Transport-Security"] = hsts_value

        # Cache control for API responses
        if not response.has_header("Cache-Control"):
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
