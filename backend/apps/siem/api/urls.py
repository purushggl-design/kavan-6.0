from django.urls import path
from apps.siem.api.views import (
    DetectionRuleListView,
    DetectionRuleDetailView,
    CorrelationRuleListView,
    SIEMStatsView,
)

app_name = 'siem'

urlpatterns = [
    path('siem/rules/', DetectionRuleListView.as_view(), name='siem-rules-list'),
    path('siem/rules/<uuid:pk>/', DetectionRuleDetailView.as_view(), name='siem-rules-detail'),
    path('siem/correlation-rules/', CorrelationRuleListView.as_view(), name='siem-correlation-rules'),
    path('siem/stats/', SIEMStatsView.as_view(), name='siem-stats'),
]
