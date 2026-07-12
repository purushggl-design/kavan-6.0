from rest_framework.routers import DefaultRouter
from .views import SIEMIntegrationConfigViewSet, SIEMRetryQueueViewSet

router = DefaultRouter()
router.register(r'integrations/siem-configs', SIEMIntegrationConfigViewSet, basename='siem-configs')
router.register(r'integrations/siem-retries', SIEMRetryQueueViewSet, basename='siem-retries')

urlpatterns = router.urls
