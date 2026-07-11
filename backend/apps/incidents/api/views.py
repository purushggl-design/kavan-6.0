from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.incidents.models.incidents import Alert, Incident, AlertStatus, IncidentStatus, IncidentActivity
from apps.incidents.api.serializers import AlertSerializer, IncidentSerializer, IncidentDetailSerializer
from apps.tenants.permissions import IsPlatformAdmin


class AlertListView(APIView):
    """
    List all alerts, optionally filtered by severity or status.
    GET /api/v1/incidents/alerts/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = AlertSerializer

    @extend_schema(
        summary="List security alerts",
        parameters=[
            OpenApiParameter('status', str, description='Filter by status: NEW, ACKNOWLEDGED, RESOLVED'),
            OpenApiParameter('severity', str, description='Filter by severity: LOW, MEDIUM, HIGH, CRITICAL'),
        ],
        responses={200: AlertSerializer(many=True)},
    )
    def get(self, request):
        qs = Alert.objects.all().order_by('-created_at')

        filter_status = request.query_params.get('status')
        filter_severity = request.query_params.get('severity')

        if filter_status:
            qs = qs.filter(status=filter_status.upper())
        if filter_severity:
            qs = qs.filter(severity=filter_severity.upper())

        serializer = AlertSerializer(qs[:100], many=True)  # cap at 100 for performance
        return Response({'success': True, 'count': qs.count(), 'data': serializer.data})


class AlertDetailView(APIView):
    """
    Retrieve a single alert and update its status (acknowledge / resolve).
    GET   /api/v1/incidents/alerts/<id>/
    PATCH /api/v1/incidents/alerts/<id>/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = AlertSerializer

    def _get_alert(self, pk):
        try:
            return Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return None

    def get(self, request, pk):
        alert = self._get_alert(pk)
        if not alert:
            return Response({'success': False, 'error': 'Alert not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': AlertSerializer(alert).data})

    @extend_schema(
        summary="Update alert status",
        request=AlertSerializer,
        responses={200: AlertSerializer},
    )
    def patch(self, request, pk):
        alert = self._get_alert(pk)
        if not alert:
            return Response({'success': False, 'error': 'Alert not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status and new_status.upper() in [AlertStatus.ACKNOWLEDGED, AlertStatus.RESOLVED]:
            alert.status = new_status.upper()
            alert.save(update_fields=['status', 'updated_at'])

        return Response({'success': True, 'data': AlertSerializer(alert).data})


class IncidentListView(APIView):
    """
    List all incidents, optionally filtered by status.
    GET /api/v1/incidents/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = IncidentSerializer

    @extend_schema(
        summary="List security incidents",
        parameters=[
            OpenApiParameter('status', str, description='Filter by status (NEW, INVESTIGATING, RESOLVED, CLOSED)'),
        ],
        responses={200: IncidentSerializer(many=True)},
    )
    def get(self, request):
        qs = Incident.objects.all().order_by('-created_at')

        filter_status = request.query_params.get('status')
        if filter_status:
            qs = qs.filter(status=filter_status.upper())

        serializer = IncidentSerializer(qs[:100], many=True)
        return Response({'success': True, 'count': qs.count(), 'data': serializer.data})

    @extend_schema(
        summary="Create a new incident",
        request=IncidentSerializer,
        responses={201: IncidentSerializer},
    )
    def post(self, request):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            incident = serializer.save()
            return Response(
                {'success': True, 'data': IncidentSerializer(incident).data},
                status=status.HTTP_201_CREATED,
            )
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IncidentDetailView(APIView):
    """
    Retrieve or update a single incident (status, assignment).
    GET   /api/v1/incidents/<id>/
    PATCH /api/v1/incidents/<id>/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = IncidentDetailSerializer

    def _get_incident(self, pk):
        try:
            return Incident.objects.prefetch_related('alerts', 'activities').get(pk=pk)
        except Incident.DoesNotExist:
            return None

    def get(self, request, pk):
        incident = self._get_incident(pk)
        if not incident:
            return Response({'success': False, 'error': 'Incident not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': IncidentDetailSerializer(incident).data})

    @extend_schema(
        summary="Update incident (status, assignment)",
        request=IncidentSerializer,
        responses={200: IncidentSerializer},
    )
    def patch(self, request, pk):
        incident = self._get_incident(pk)
        if not incident:
            return Response({'success': False, 'error': 'Incident not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        notes = request.data.get('notes', '')

        allowed_statuses = [s.value for s in IncidentStatus]
        if new_status and new_status.upper() in allowed_statuses:
            old_status = incident.status
            incident.status = new_status.upper()
            incident.save(update_fields=['status', 'updated_at'])

            # Log the status change as an activity
            IncidentActivity.objects.create(
                incident=incident,
                user=request.user,
                action=f"Status changed: {old_status} → {incident.status}",
                notes=notes,
            )

        return Response({'success': True, 'data': IncidentDetailSerializer(incident).data})
