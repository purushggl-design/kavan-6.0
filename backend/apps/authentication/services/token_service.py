import hashlib
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple, Optional

import jwt
from django.conf import settings
from django.core.cache import cache

from apps.authentication.models import User, RefreshToken


class TokenException(Exception):
    pass


class TokenService:
    """
    Enterprise token management service handling JWT generation, validation, 
    and Redis-based blacklisting for strict access control.
    """
    
    # Defaults; in a real app, load from config
    ACCESS_TOKEN_TTL = getattr(settings, 'JWT_ACCESS_TOKEN_TTL', 900)  # 15 mins
    REFRESH_TOKEN_TTL = getattr(settings, 'JWT_REFRESH_TOKEN_TTL', 2592000)  # 30 days
    SECRET_KEY = settings.SECRET_KEY
    ISSUER = getattr(settings, 'JWT_ISSUER', 'KAVAN')
    ALGORITHM = 'HS256' # Configurable for RS256 migration
    
    @classmethod
    def generate_tokens(cls, user: User, device_id: Optional[str] = None, ip_address: Optional[str] = None) -> Tuple[str, str, datetime]:
        """
        Generates a new access token and refresh token pair for a user.
        Records the refresh token in the database for rotation tracking.
        """
        jti = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=cls.ACCESS_TOKEN_TTL)
        
        # 1. Generate Access Token (JWT)
        access_payload = {
            'iss': cls.ISSUER,
            'sub': str(user.id),
            'jti': jti,
            'iat': int(now.timestamp()),
            'exp': int(expires_at.timestamp()),
            'type': 'access',
            'mfa_verified': getattr(user, 'mfa_enabled', False) # Simplified
        }
        
        access_token = jwt.encode(access_payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        
        # 2. Generate Refresh Token (Opaque string or JWT, we'll use a secure random UUID)
        raw_refresh_token = f"{uuid.uuid4().hex}{uuid.uuid4().hex}"
        refresh_token_hash = cls._hash_token(raw_refresh_token)
        
        rt_expires_at = now + timedelta(seconds=cls.REFRESH_TOKEN_TTL)
        
        # Store refresh token
        RefreshToken.objects.create(
            user=user,
            token_hash=refresh_token_hash,
            device_id=device_id,
            ip_address=ip_address,
            expires_at=rt_expires_at
        )
        
        return access_token, raw_refresh_token, expires_at
        
    @classmethod
    def validate_access_token(cls, token: str) -> Dict[str, Any]:
        """
        Validates an access token signature, expiration, and checks the blacklist.
        Returns the decoded payload if valid.
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM], issuer=cls.ISSUER)
            
            # Check blacklist
            jti = payload.get('jti')
            if jti and cache.get(f"blacklist_{jti}"):
                raise TokenException("Token has been blacklisted")
                
            return payload
            
        except jwt.ExpiredSignatureError:
            raise TokenException("Token has expired")
        except jwt.InvalidTokenError as e:
            raise TokenException(f"Invalid token: {str(e)}")

    @classmethod
    def rotate_refresh_token(cls, raw_refresh_token: str, ip_address: Optional[str] = None) -> Tuple[str, str, datetime, User]:
        """
        Validates the given refresh token and issues a new token pair (rotation).
        If the token was already revoked, this indicates a potential replay attack
        and we will revoke ALL tokens for this user.
        """
        token_hash = cls._hash_token(raw_refresh_token)
        
        try:
            rt_record = RefreshToken.objects.get(token_hash=token_hash)
        except RefreshToken.DoesNotExist:
            raise TokenException("Invalid refresh token")
            
        # Check if already revoked
        if rt_record.is_revoked:
            # Token reuse detected! Revoke all tokens for this user for safety
            RefreshToken.objects.filter(user=rt_record.user, is_revoked=False).update(
                is_revoked=True,
                revoked_at=datetime.now(timezone.utc)
            )
            raise TokenException("Token reuse detected. All sessions revoked for security.")
            
        # Check expiration
        if rt_record.expires_at < datetime.now(timezone.utc):
            raise TokenException("Refresh token expired")
            
        # Revoke the current token
        rt_record.is_revoked = True
        rt_record.revoked_at = datetime.now(timezone.utc)
        rt_record.save(update_fields=['is_revoked', 'revoked_at'])
        
        # Issue new tokens
        access, refresh, exp = cls.generate_tokens(
            user=rt_record.user, 
            device_id=rt_record.device_id,
            ip_address=ip_address
        )
        
        return access, refresh, exp, rt_record.user

    @classmethod
    def blacklist_access_token(cls, token: str) -> None:
        """
        Adds an access token to the Redis blacklist until its natural expiration.
        """
        try:
            # We don't verify expiration here since we might want to blacklist an already expired token,
            # but usually we just decode without verification to get the JTI and EXP.
            payload = jwt.decode(token, options={"verify_signature": False})
            jti = payload.get('jti')
            exp = payload.get('exp')
            
            if not jti or not exp:
                return
                
            now = int(time.time())
            ttl = exp - now
            
            if ttl > 0:
                cache.set(f"blacklist_{jti}", "1", timeout=ttl)
                
        except jwt.InvalidTokenError:
            pass

    @classmethod
    def _hash_token(cls, token: str) -> str:
        """Returns SHA-256 hash of a string token."""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()
