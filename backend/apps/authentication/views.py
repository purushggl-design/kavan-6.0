from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.authentication.serializers.auth import (
    LoginSerializer, RegisterSerializer, RefreshTokenSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, VerifyEmailSerializer,
    MFASerializer
)
from apps.authentication.services.auth_service import AuthService, AuthenticationException
from config.exceptions.auth import InvalidCredentialsException
from apps.authentication.services.token_service import TokenService, TokenException
from apps.authentication.services.mfa_service import MFAService
from common.responses.standard_response import StandardResponse
from rest_framework import serializers

class EmptySerializer(serializers.Serializer):
    pass

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Login",
        description="Authenticates a user and returns JWT access and refresh tokens.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Successful login"),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Invalid credentials")
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = AuthService.login(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                mfa_code=serializer.validated_data.get('mfa_code'),
                request_meta=request.META
            )
            return StandardResponse.success(data=data, message="Login successful")
        except AuthenticationException as e:
            if str(e) == "MFA_REQUIRED":
                return StandardResponse.error("MFA code required.", status=status.HTTP_401_UNAUTHORIZED, code="MFA_REQUIRED")
            return StandardResponse.error(str(e), status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Registration",
        description="Registers a new user and sends an email verification link.",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Registration successful"),
            400: OpenApiResponse(description="Validation error or user exists")
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = AuthService.register(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                request_meta=request.META
            )
            return StandardResponse.success(message="Registration successful. Please verify your email.", status=status.HTTP_201_CREATED)
        except AuthenticationException as e:
            return StandardResponse.error(str(e), status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        summary="User Logout",
        description="Logs out a user and blacklists their current refresh token.",
        responses={
            200: OpenApiResponse(description="Logout successful"),
            401: OpenApiResponse(description="Authentication credentials were not provided or are invalid")
        }
    )
    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        access_token = auth_header.split(' ')[1] if ' ' in auth_header else ''
        refresh_token = request.data.get('refresh_token', '')

        AuthService.logout(
            user=request.user,
            access_token=access_token,
            refresh_token_raw=refresh_token,
            request_meta=request.META
        )
        return StandardResponse.success(message="Logout successful")


class RefreshAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh JWT Token",
        description="Provides a new access token and refresh token based on a valid refresh token.",
        request=RefreshTokenSerializer,
        responses={
            200: OpenApiResponse(description="Tokens refreshed"),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Invalid or expired refresh token")
        }
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            access, refresh, expires_at, user = TokenService.rotate_refresh_token(
                raw_refresh_token=serializer.validated_data['refresh_token'],
                ip_address=request.META.get("REMOTE_ADDR")
            )
            return StandardResponse.success(message="Token refreshed successfully", data={
                "access_token": access,
                "refresh_token": refresh,
                "expires_at": expires_at.isoformat()
            })
        except TokenException as e:
            return StandardResponse.error(str(e), status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Forgot Password",
        description="Sends a password reset link to the user's email if it exists.",
        request=ForgotPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Reset link sent successfully (or silently ignored if not found)"),
            400: OpenApiResponse(description="Validation error")
        }
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        AuthService.forgot_password(
            email=serializer.validated_data['email'],
            request_meta=request.META
        )
        return StandardResponse.success(message="If the email exists, a reset link has been sent.")


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Reset Password",
        description="Resets the password using the token sent to the user's email.",
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password reset successfully"),
            400: OpenApiResponse(description="Validation error or invalid/expired token")
        }
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            AuthService.reset_password(
                token=serializer.validated_data['token'],
                new_password=serializer.validated_data['password'],
                request_meta=request.META
            )
            return StandardResponse.success(message="Password reset successfully.")
        except AuthenticationException as e:
            return StandardResponse.error(str(e), status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Verify Email",
        description="Verifies the user's email using a token.",
        request=VerifyEmailSerializer,
        responses={
            200: OpenApiResponse(description="Email verified successfully"),
            400: OpenApiResponse(description="Validation error or invalid token")
        }
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Call AuthService (stubbed logic for now)
        return StandardResponse.success(message="Email verified successfully.")

class MFASetupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        summary="MFA Setup",
        description="Initiates MFA setup by generating a secret and returning a QR code URI.",
        responses={
            200: OpenApiResponse(description="Returns OTP URI and base64 QR code")
        }
    )
    def post(self, request):
        otp_uri = MFAService.initiate_setup(request.user)
        qr_code = MFAService.get_qr_code_base64(otp_uri)
        return StandardResponse.success(
            data={"otp_uri": otp_uri, "qr_code_base64": qr_code}, 
            message="MFA setup initiated. Please verify with an OTP."
        )

class MFAVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="MFA Verify Setup",
        description="Verifies the OTP during MFA setup and activates MFA.",
        request=MFASerializer,
        responses={
            200: OpenApiResponse(description="MFA verified successfully, returns backup codes"),
            400: OpenApiResponse(description="Invalid OTP")
        }
    )
    def post(self, request):
        serializer = MFASerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error("Validation Failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            backup_codes = MFAService.verify_setup(request.user, serializer.validated_data['otp'])
            return StandardResponse.success(
                data={"backup_codes": backup_codes},
                message="MFA verified and activated successfully. Please save these backup codes."
            )
        except (AuthenticationException, InvalidCredentialsException) as e:
            return StandardResponse.error(str(e), status=status.HTTP_400_BAD_REQUEST)

class MFADisableAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        summary="MFA Disable",
        description="Disables MFA for the current user.",
        responses={
            200: OpenApiResponse(description="MFA disabled successfully")
        }
    )
    def post(self, request):
        MFAService.disable_mfa(request.user)
        return StandardResponse.success(message="MFA disabled successfully.")

class MFARegenerateBackupCodesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @extend_schema(
        summary="Regenerate Backup Codes",
        description="Invalidates old backup codes and generates new ones.",
        responses={
            200: OpenApiResponse(description="Backup codes regenerated")
        }
    )
    def post(self, request):
        if not request.user.mfa_enabled:
            return StandardResponse.error("MFA is not enabled.", status=status.HTTP_400_BAD_REQUEST)
            
        backup_codes = MFAService.generate_backup_codes(request.user)
        return StandardResponse.success(
            data={"backup_codes": backup_codes},
            message="Backup codes regenerated successfully."
        )

class OAuthLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    @extend_schema(
        summary="OAuth Login",
        description="Authenticates a user via OAuth provider (e.g. Google, Microsoft).",
        responses={200: OpenApiResponse(description="OAuth login successful")}
    )
    def post(self, request):
        # Stub implementation
        return StandardResponse.success(data={"access_token": "mock_oauth_jwt"}, message="OAuth login successful.")
