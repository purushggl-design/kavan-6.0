from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MFAVerifySerializer, MFASetupResponseSerializer

class MFAViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def setup(self, request):
        """Initiate MFA setup."""
        # Stub logic
        data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_url": "otpauth://totp/KAVAN:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=KAVAN",
            "backup_codes": ["12345678", "87654321"]
        }
        return Response({
            "success": True,
            "message": "MFA setup initiated.",
            "data": data,
            "errors": None,
            "meta": {}
        })

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify the MFA setup code."""
        serializer = MFAVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Validation Failed",
                "data": None,
                "errors": serializer.errors,
                "meta": {}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "success": True,
            "message": "MFA verified successfully.",
            "data": {"verified": True},
            "errors": None,
            "meta": {}
        })

    @action(detail=False, methods=['post'])
    def disable(self, request):
        """Disable MFA for the user."""
        return Response({
            "success": True,
            "message": "MFA disabled successfully.",
            "data": {"disabled": True},
            "errors": None,
            "meta": {}
        })
