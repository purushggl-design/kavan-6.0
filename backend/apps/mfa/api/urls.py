from rest_framework.routers import DefaultRouter
from .views import MFAViewSet

router = DefaultRouter()
router.register(r'mfa', MFAViewSet, basename='mfa')

urlpatterns = router.urls
