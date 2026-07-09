import base64
import hashlib
import os
import secrets
from datetime import datetime
from io import BytesIO

import pyotp
import qrcode
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone

from apps.authentication.models import User
from apps.mfa.models import BackupCode, MFASecret
from config.exceptions.auth import InvalidCredentialsException


class MFAService:
    @staticmethod
    def _get_fernet() -> Fernet:
        # Derive a 32-byte key from settings.SECRET_KEY
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        return Fernet(base64.urlsafe_b64encode(key))

    @staticmethod
    def _encrypt_secret(secret: str) -> str:
        f = MFAService._get_fernet()
        return f.encrypt(secret.encode()).decode()

    @staticmethod
    def _decrypt_secret(encrypted_secret: str) -> str:
        f = MFAService._get_fernet()
        return f.decrypt(encrypted_secret.encode()).decode()

    @staticmethod
    def initiate_setup(user: User) -> str:
        """
        Generates a new TOTP secret for the user and saves it as inactive.
        Returns the OTP Auth URI for generating a QR code.
        """
        secret = pyotp.random_base32()
        
        # Replace existing secret if user is re-setting up
        if hasattr(user, 'mfa_secret'):
            user.mfa_secret.delete()

        MFASecret.objects.create(
            user=user,
            secret_encrypted=MFAService._encrypt_secret(secret),
            is_active=False
        )
        
        totp = pyotp.TOTP(secret)
        otp_uri = totp.provisioning_uri(name=user.email, issuer_name="KAVAN")
        return otp_uri
        
    @staticmethod
    def get_qr_code_base64(otp_uri: str) -> str:
        """
        Converts an OTP URI to a base64 encoded PNG image of the QR code.
        """
        qr = qrcode.make(otp_uri)
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    @staticmethod
    def verify_setup(user: User, code: str) -> list[str]:
        """
        Verifies the code during setup and activates MFA.
        Returns a list of backup codes.
        """
        if not hasattr(user, 'mfa_secret') or user.mfa_secret.is_active:
            raise InvalidCredentialsException("MFA setup is not in progress.")

        secret = MFAService._decrypt_secret(user.mfa_secret.secret_encrypted)
        totp = pyotp.TOTP(secret)
        
        if not totp.verify(code):
            raise InvalidCredentialsException("Invalid OTP code.")

        user.mfa_secret.is_active = True
        user.mfa_secret.verified_at = timezone.now()
        user.mfa_secret.save()
        
        user.mfa_enabled = True
        user.save(update_fields=['mfa_enabled'])
        
        return MFAService.generate_backup_codes(user)

    @staticmethod
    def verify_login(user: User, code: str) -> bool:
        """
        Verifies an OTP code for login. Also accepts valid backup codes.
        """
        if not hasattr(user, 'mfa_secret') or not user.mfa_secret.is_active:
            return False

        # Try OTP
        secret = MFAService._decrypt_secret(user.mfa_secret.secret_encrypted)
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            return True
            
        # Try Backup Code
        if len(code) == 8:
            code_hash = hashlib.sha256(code.encode()).hexdigest()
            backup = BackupCode.objects.filter(user=user, is_used=False, code_hash=code_hash).first()
            if backup:
                backup.is_used = True
                backup.used_at = timezone.now()
                backup.save()
                return True
                
        return False

    @staticmethod
    def disable_mfa(user: User):
        """
        Disables MFA for the user and removes secrets and backup codes.
        """
        if hasattr(user, 'mfa_secret'):
            user.mfa_secret.delete()
        
        BackupCode.objects.filter(user=user).delete()
        
        user.mfa_enabled = False
        user.save(update_fields=['mfa_enabled'])

    @staticmethod
    def generate_backup_codes(user: User) -> list[str]:
        """
        Invalidates existing backup codes and generates 10 new ones.
        Returns the plain text codes (these are only returned once!).
        """
        BackupCode.objects.filter(user=user, is_used=False).update(
            is_used=True, 
            used_at=timezone.now()
        )
        
        plain_codes = []
        objects_to_create = []
        
        for _ in range(10):
            code = secrets.token_hex(4) # 8 chars
            plain_codes.append(code)
            code_hash = hashlib.sha256(code.encode()).hexdigest()
            objects_to_create.append(BackupCode(user=user, code_hash=code_hash))
            
        BackupCode.objects.bulk_create(objects_to_create)
        return plain_codes
