from django.urls import path
from apps.authentication.views import (
    LoginAPIView, RegisterAPIView, LogoutAPIView, RefreshAPIView,
    ForgotPasswordAPIView, ResetPasswordAPIView, VerifyEmailAPIView,
    MFASetupAPIView, MFAVerifyAPIView, MFADisableAPIView,
    MFARegenerateBackupCodesAPIView, OAuthLoginAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('mfa/setup/', MFASetupAPIView.as_view(), name='mfa-setup'),
    path('mfa/verify/', MFAVerifyAPIView.as_view(), name='mfa-verify'),
    path('mfa/disable/', MFADisableAPIView.as_view(), name='mfa-disable'),
    path('mfa/backup-codes/', MFARegenerateBackupCodesAPIView.as_view(), name='mfa-backup-codes'),
    path('oauth/login/', OAuthLoginAPIView.as_view(), name='oauth-login'),
]
