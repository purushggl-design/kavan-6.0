"""
KAVAN v6.0 — Rate Limiting Foundation
============================================================
Defines custom throttles for Anonymous, Authenticated Users, and Burst prevention.
Gated by ENABLE_RATE_LIMIT feature flag.
"""

from rest_framework.throttling import SimpleRateThrottle
from config.feature_flags import ENABLE_RATE_LIMIT

class KavanAnonRateThrottle(SimpleRateThrottle):
    """
    Limits requests from anonymous users based on client IP.
    """
    scope = "anon"

    def allow_request(self, request, view) -> bool:
        if not ENABLE_RATE_LIMIT:
            return True
        return super().allow_request(request, view)


class KavanUserRateThrottle(SimpleRateThrottle):
    """
    Limits requests from authenticated users. Falls back to IP.
    """
    scope = "user"

    def allow_request(self, request, view) -> bool:
        if not ENABLE_RATE_LIMIT:
            return True
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = str(request.user.pk)
        else:
            ident = self.get_ident(request)
            
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident
        }


class KavanBurstThrottle(SimpleRateThrottle):
    """
    Saves the server from sudden request spikes (burst traffic).
    """
    scope = "burst"

    def allow_request(self, request, view) -> bool:
        if not ENABLE_RATE_LIMIT:
            return True
        return super().allow_request(request, view)
