from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.audit.api.views import AuditViewSet

app_name = 'audit'
router = DefaultRouter()
router.register(r'', AuditViewSet, basename='audit')

urlpatterns = [
    path('', include(router.urls)),
]
