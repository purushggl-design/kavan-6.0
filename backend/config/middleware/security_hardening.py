"""
KAVAN v6.0 — Security Hardening Middleware
============================================================
Hardens HTTP endpoints by restricting request payloads, enforcing Host checking,
and applying strict Content Security Policies (CSP).
"""

import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import SuspiciousOperation

logger = logging.getLogger("kavan.security")

class SecurityHardeningMiddleware:
    """
    Enforces strict operational boundaries on incoming requests and outgoing headers.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_body_bytes = getattr(settings, "MAX_UPLOAD_SIZE", 10 * 1024 * 1024)  # 10 MB default

    def __call__(self, request):
        # 1. Enforce payload size limit
        content_length = request.META.get("CONTENT_LENGTH")
        if content_length:
            try:
                if int(content_length) > self.max_body_bytes:
                    logger.warning(
                        "Payload size limit exceeded",
                        extra={
                            "kavan_data": {
                                "client_ip": request.META.get("REMOTE_ADDR"),
                                "content_length": content_length,
                                "max_limit": self.max_body_bytes,
                            }
                        }
                    )
                    return HttpResponse("Request Entity Too Large", status=413)
            except ValueError:
                return HttpResponseBadRequest("Invalid Content-Length Header")

        # 2. Host Validation check
        host = request.get_host().split(":")[0]
        allowed_hosts = getattr(settings, "ALLOWED_HOSTS", [])
        
        if not getattr(settings, "DEBUG", False) and allowed_hosts and "*" not in allowed_hosts:
            if host not in allowed_hosts and "localhost" not in allowed_hosts:
                logger.error(
                    f"Suspicious host header received: {host}",
                    extra={"kavan_data": {"host": host, "allowed": allowed_hosts}}
                )
                raise SuspiciousOperation(f"Invalid Host Header: {host}")

        # Execute down the middleware chain
        response = self.get_response(request)

        # 3. Strict Content-Security-Policy (CSP) headers injection
        csp_rules = [
            "default-src 'none'",
            "script-src 'self'",
            "connect-src 'self' https://* ws://* wss://*",
            "img-src 'self' data: https:",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response["Content-Security-Policy"] = "; ".join(csp_rules)

        # 4. Referrer Policy & Permissions
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=()"

        # 5. Security Header safeguards
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"

        return response
