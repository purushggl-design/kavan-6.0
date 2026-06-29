from django.contrib.auth import authenticate
from django.utils import timezone
from typing import Dict, Any, Optional

from backend.apps.authentication.models import User
from backend.apps.authentication.services.token_service import TokenService

class AuthenticationException(Exception):
    pass

class AuthService:
    """
    Core service orchestrating authentication business logic independent of the web layer.
    """
    
    @classmethod
    def login(cls, email: str, password: str, request_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validates credentials and issues tokens.
        Includes password history and lockout checks implicitly handled by the User model or here.
        """
        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationException("Invalid email or password.")
            
        if not user.is_active:
            raise AuthenticationException("Account is disabled.")
            
        # TODO: Implement lockouts, password expiry checks, MFA trigger here
        
        # Track session / login event (Audit Logging)
        cls._log_audit(user, "LOGIN_SUCCESS", request_meta)
        
        ip_address = request_meta.get("REMOTE_ADDR") if request_meta else None
        
        access_token, refresh_token, expires_at = TokenService.generate_tokens(
            user=user, 
            ip_address=ip_address
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat(),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "mfa_required": getattr(user, 'mfa_enabled', False)
        }

    @classmethod
    def logout(cls, user: User, access_token: str, refresh_token_raw: str, request_meta: Optional[Dict[str, Any]] = None) -> None:
        """
        Invalidates tokens and closes session.
        """
        # Blacklist current access token
        TokenService.blacklist_access_token(access_token)
        
        # Revoke the specific refresh token if provided
        if refresh_token_raw:
            try:
                # We can just rotate it to revoke, but we ignore the new tokens. 
                # Better to have a explicit revoke method, but this suffices for the MVP.
                # A proper implementation would find the RefreshToken by hash and set is_revoked=True
                token_hash = TokenService._hash_token(refresh_token_raw)
                from backend.apps.authentication.models import RefreshToken
                rt = RefreshToken.objects.filter(token_hash=token_hash).first()
                if rt:
                    rt.is_revoked = True
                    rt.revoked_at = timezone.now()
                    rt.save()
            except Exception:
                pass
                
        cls._log_audit(user, "LOGOUT", request_meta)
        
    @classmethod
    def _log_audit(cls, user: User, action: str, request_meta: Optional[Dict[str, Any]]) -> None:
        """
        Helper to log authentication events. 
        In full implementation, this writes to the Audit log model.
        """
        pass # To be fully wired with the audit app
