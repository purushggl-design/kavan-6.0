"""
KAVAN v6.0 — Root URL Configuration
============================================================
URL routing hierarchy:
  /admin/          → Django admin
  /health/         → Health check endpoints (Layer 1)
  /api/v1/         → REST API version 1 (Layer 2+)
  /api/v2/         → REST API version 2 (future)
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from config.feature_flags import ENABLE_SWAGGER

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Health Check Endpoints (Layer 1)
    path("health/", include("apps.health.urls", namespace="health")),

    # API v1 (Layer 2+ will add routes here)
    path("api/v1/", include("config.api_router", namespace="api_v1")),
]

# OpenAPI documentation routes
if ENABLE_SWAGGER:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


