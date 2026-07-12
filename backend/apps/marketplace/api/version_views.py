from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.marketplace.models.application import ApplicationVersion
from apps.marketplace.api.serializers import ApplicationVersionSerializer
from apps.rbac.permissions.decorators import HasPlatformPermission

class ApplicationVersionUploadView(generics.CreateAPIView):
    """
    POST /api/v1/marketplace/versions/
    Registers a new application version (image pushed, manifest uploaded).
    Requires 'marketplace:publish' platform permission (Developer / SuperAdmin).
    """
    queryset = ApplicationVersion.objects.all()
    serializer_class = ApplicationVersionSerializer
    permission_classes = [HasPlatformPermission("marketplace:publish")()]

    @extend_schema(
        summary="Upload/Register Application Version",
        description="Registers a new version of an application with its manifest for provisioning.",
        request=ApplicationVersionSerializer,
        responses={201: ApplicationVersionSerializer}
    )
    def create(self, request, *args, **kwargs):
        # DRF automatically calls serializer.is_valid() which in turn triggers 
        # the model's manifest validation logic that we defined.
        return super().create(request, *args, **kwargs)
