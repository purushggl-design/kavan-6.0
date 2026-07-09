from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.devices.api.views import DeviceViewSet

app_name = 'devices'
router = DefaultRouter()
router.register(r'', DeviceViewSet, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
]
