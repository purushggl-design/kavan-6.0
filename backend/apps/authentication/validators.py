import re
from typing import Optional
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator:
    """
    Validates that a password meets enterprise security standards.
    """
    
    @classmethod
    def validate(cls, password: str, user=None) -> None:
        """
        Validates the password strength.
        Raises ValidationError if any check fails.
        """
        if len(password) < 12:
            raise ValidationError(_("Password must be at least 12 characters long."), code='password_too_short')
            
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter."), code='password_no_upper')
            
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must contain at least one lowercase letter."), code='password_no_lower')
            
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("Password must contain at least one digit."), code='password_no_digit')
            
        if not re.search(r'[\W_]', password):
            raise ValidationError(_("Password must contain at least one special character."), code='password_no_special')
            
        # Check password history if user is provided
        if user:
            from django.contrib.auth.hashers import check_password
            from apps.accounts.models import PasswordHistory
            from config.auth_config import AuthConfig
            
            # Fetch last N password history records
            history = PasswordHistory.objects.filter(user=user)[:AuthConfig.PASSWORD_HISTORY_LIMIT]
            for record in history:
                if check_password(password, record.password_hash):
                    raise ValidationError(
                        _("Password has been used recently. Please choose a different password."),
                        code='password_reused'
                    )
