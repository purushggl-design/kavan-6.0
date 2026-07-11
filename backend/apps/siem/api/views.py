from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.siem.models.rules import DetectionRule, CorrelationRule
from apps.siem.api.serializers import DetectionRuleSerializer, CorrelationRuleSerializer
from apps.tenants.permissions import IsPlatformAdmin


class DetectionRuleListView(APIView):
    """
    List all detection rules or create a new one.
    GET  /api/v1/siem/rules/
    POST /api/v1/siem/rules/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = DetectionRuleSerializer

    @extend_schema(
        summary="List SIEM detection rules",
        responses={200: DetectionRuleSerializer(many=True)},
    )
    def get(self, request):
        active_only = request.query_params.get('active', None)
        qs = DetectionRule.objects.all().order_by('-created_at')
        if active_only == 'true':
            qs = qs.filter(is_active=True)
        serializer = DetectionRuleSerializer(qs, many=True)
        return Response({'success': True, 'data': serializer.data})

    @extend_schema(
        summary="Create a SIEM detection rule",
        request=DetectionRuleSerializer,
        responses={201: DetectionRuleSerializer},
    )
    def post(self, request):
        serializer = DetectionRuleSerializer(data=request.data)
        if serializer.is_valid():
            rule = serializer.save()
            return Response(
                {'success': True, 'data': DetectionRuleSerializer(rule).data},
                status=status.HTTP_201_CREATED,
            )
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DetectionRuleDetailView(APIView):
    """
    Retrieve, update, or delete a detection rule.
    GET    /api/v1/siem/rules/<id>/
    PATCH  /api/v1/siem/rules/<id>/
    DELETE /api/v1/siem/rules/<id>/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = DetectionRuleSerializer

    def _get_rule(self, pk):
        try:
            return DetectionRule.objects.get(pk=pk)
        except DetectionRule.DoesNotExist:
            return None

    def get(self, request, pk):
        rule = self._get_rule(pk)
        if not rule:
            return Response({'success': False, 'error': 'Rule not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': DetectionRuleSerializer(rule).data})

    def patch(self, request, pk):
        rule = self._get_rule(pk)
        if not rule:
            return Response({'success': False, 'error': 'Rule not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DetectionRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rule = self._get_rule(pk)
        if not rule:
            return Response({'success': False, 'error': 'Rule not found.'}, status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response({'success': True, 'message': 'Rule deleted.'}, status=status.HTTP_204_NO_CONTENT)


class CorrelationRuleListView(APIView):
    """
    List all correlation rules.
    GET /api/v1/siem/correlation-rules/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]
    serializer_class = CorrelationRuleSerializer

    def get(self, request):
        qs = CorrelationRule.objects.all().order_by('-created_at')
        serializer = CorrelationRuleSerializer(qs, many=True)
        return Response({'success': True, 'data': serializer.data})

    def post(self, request):
        serializer = CorrelationRuleSerializer(data=request.data)
        if serializer.is_valid():
            rule = serializer.save()
            return Response(
                {'success': True, 'data': CorrelationRuleSerializer(rule).data},
                status=status.HTTP_201_CREATED,
            )
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SIEMStatsView(APIView):
    """
    High-level SIEM statistics for the platform dashboard.
    GET /api/v1/siem/stats/
    """
    permission_classes = [IsAuthenticated, IsPlatformAdmin]

    from rest_framework import serializers as drf_serializers

    class _EmptySerializer(drf_serializers.Serializer):
        pass

    serializer_class = _EmptySerializer

    def get(self, request):
        from apps.incidents.models.incidents import Alert, Incident, AlertStatus, IncidentStatus
        total_rules = DetectionRule.objects.count()
        active_rules = DetectionRule.objects.filter(is_active=True).count()
        correlation_rules = CorrelationRule.objects.count()
        new_alerts = Alert.objects.filter(status=AlertStatus.NEW).count()
        open_incidents = Incident.objects.exclude(status=IncidentStatus.CLOSED).count()

        return Response({
            'success': True,
            'data': {
                'detection_rules': {'total': total_rules, 'active': active_rules},
                'correlation_rules': correlation_rules,
                'alerts': {'new': new_alerts},
                'incidents': {'open': open_incidents},
            },
        })
