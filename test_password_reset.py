import os
import django
import sys
import hashlib
from django.utils import timezone
import datetime

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.authentication.services.auth_service import AuthService, AuthenticationException
from apps.authentication.models import User, PasswordReset

user = User.objects.first()
if not user:
    user = User.objects.create(email="test@kavan.com")
    user.set_password("Admin123!")
    user.save()
user_email = user.email

print("--- TEST 1: REJECT INVALID TOKEN ---")
try:
    AuthService.reset_password("totally_made_up_token_123", "NewStrongP@ssw0rd!")
    print("FAIL: Accepted invalid token?!")
except AuthenticationException as e:
    print(f"SUCCESS: Rejected invalid token with error: {str(e)}")

print("\n--- TEST 2: GENERATE AND USE REAL TOKEN ---")
# Manually create a token in the DB to simulate forgot_password
raw_token = "my_super_secret_token_456"
token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
PasswordReset.objects.create(
    user=user,
    token_hash=token_hash,
    expires_at=timezone.now() + datetime.timedelta(minutes=15)
)
print("Token inserted into DB: my_super_secret_token_456")

try:
    AuthService.reset_password("my_super_secret_token_456", "Admin123!New12345")
    print("SUCCESS: Password reset successfully using valid token.")
except Exception as e:
    print(f"FAIL: {str(e)}")

print("\n--- TEST 3: REJECT USED TOKEN ---")
try:
    AuthService.reset_password("my_super_secret_token_456", "Admin123!New54321")
    print("FAIL: Accepted used token?!")
except AuthenticationException as e:
    print(f"SUCCESS: Rejected used token with error: {str(e)}")

print("\n--- TEST 4: CLEANUP (Revert password) ---")
try:
    # Set it back without going through the token flow again for speed
    user.set_password("Admin123!")
    user.save()
    print("SUCCESS: Password reverted to original.")
except Exception as e:
    print(f"FAIL: {str(e)}")
