from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.api.views import AccountViewSet

app_name = 'accounts'
router = DefaultRouter()
router.register(r'', AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]
