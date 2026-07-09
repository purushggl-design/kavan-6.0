from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from common.responses.standard_response import StandardResponse
from apps.profiles.services.profile_service import ProfileService
from apps.profiles.api.serializers import UserProfileSerializer
from apps.rbac.permissions.decorators import HasPlatformPermission

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProfileService()
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), HasPlatformPermission("profile:update")()]
        # Currently no specific permission needed for viewing own profile, but we can secure it.
        # As per the prompt, profile:update was listed. I will leave list with just IsAuthenticated.
        return super().get_permissions()
        
    @extend_schema(summary="Get My Profile", responses={200: UserProfileSerializer})
    def list(self, request):
        # We use list to return the singular profile of the current user for REST compliance on /profile/
        profile = self.service.get_my_profile(request.user.id)
        serializer = UserProfileSerializer(profile)
        return StandardResponse.success(data=serializer.data)
        
    @extend_schema(summary="Update My Profile", request=UserProfileSerializer, responses={200: UserProfileSerializer})
    def create(self, request):
        # We use create to update the singular profile of the current user on /profile/ (POST)
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(message="Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        profile = self.service.update_my_profile(request.user.id, serializer.validated_data)
        return StandardResponse.success(data=UserProfileSerializer(profile).data)
