from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.authentication.services.token_service import TokenService, TokenException
from apps.authentication.models import User

class JWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that validates JWTs using TokenService.
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith(self.keyword + ' '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = TokenService.validate_access_token(token)
            user_id = payload.get('sub')
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise AuthenticationFailed("User account is disabled.")
            return (user, token)
        except TokenException as e:
            raise AuthenticationFailed(str(e))
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")

    def authenticate_header(self, request):
        return self.keyword
