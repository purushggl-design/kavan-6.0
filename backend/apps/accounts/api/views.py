from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from common.responses.standard_response import StandardResponse
from apps.rbac.permissions.decorators import HasPlatformPermission
from apps.accounts.services.account_service import AccountService
from apps.accounts.api.serializers import UserSerializer, UserUpdateSerializer
from apps.authentication.models import User

class AccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AccountService()
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), HasPlatformPermission("accounts:view")()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), HasPlatformPermission("accounts:update")()]
        return super().get_permissions()
        
    @extend_schema(summary="List Users", responses={200: UserSerializer(many=True)})
    def list(self, request):
        users = self.service.list_users()
        serializer = UserSerializer(users, many=True)
        return StandardResponse.success(data=serializer.data)
        
    @extend_schema(summary="Get User", responses={200: UserSerializer})
    def retrieve(self, request, pk=None):
        user = self.service.get_user(pk)
        serializer = UserSerializer(user)
        return StandardResponse.success(data=serializer.data)
        
    @extend_schema(summary="Update User", request=UserUpdateSerializer, responses={200: UserSerializer})
    def update(self, request, pk=None):
        serializer = UserUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(message="Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.service.update_user(pk, serializer.validated_data)
        return StandardResponse.success(data=UserSerializer(user).data)
