# ============================================================
# KAVAN v6.0 — drf-spectacular Settings
# ============================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "KAVAN API",
    "DESCRIPTION": "KAVAN v6.0 Enterprise Multi-tenant Product Launch & Management Platform Infrastructure API",
    "VERSION": "6.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "displayRequestDuration": True,
        "persistAuthorization": True,
    },
    # Envelope structure can be defined here or handled via custom serializers
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
}
