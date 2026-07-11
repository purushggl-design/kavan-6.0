from django.urls import path
from apps.incidents.api.views import (
    AlertListView,
    AlertDetailView,
    IncidentListView,
    IncidentDetailView,
)

app_name = 'incidents'

urlpatterns = [
    path('incidents/alerts/', AlertListView.as_view(), name='alert-list'),
    path('incidents/alerts/<uuid:pk>/', AlertDetailView.as_view(), name='alert-detail'),
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incidents/<uuid:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
]
