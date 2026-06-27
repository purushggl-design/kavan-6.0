"""
KAVAN v6.0 — Authentication Configuration
============================================================
Centralised security settings for Layer 2 IAM.
All values are read from environment variables with safe defaults.

Import via:
    from config.auth_config import AuthConfig
"""

from decouple import config as env


class AuthConfig:
    """
    Static configuration class for all Layer 2 security settings.
    Access as: AuthConfig.JWT_ACCESS_TOKEN_TTL
    """

    # --------------------------------------------------------
    # JWT Settings
    # --------------------------------------------------------
    JWT_ALGORITHM: str = "RS256"
    JWT_ISSUER: str = env("JWT_ISSUER", default="KAVAN")
    JWT_AUDIENCE: str = env("JWT_AUDIENCE", default="KAVAN-API")
    JWT_SERVICE_AUDIENCE: str = "KAVAN-INTERNAL"

    # Access token lifetime: 15 minutes (seconds)
    JWT_ACCESS_TOKEN_TTL: int = env("JWT_ACCESS_TOKEN_TTL", default=60 * 15, cast=int)

    # Refresh token lifetime: 30 days (seconds)
    JWT_REFRESH_TOKEN_TTL: int = env(
        "JWT_REFRESH_TOKEN_TTL", default=60 * 60 * 24 * 30, cast=int
    )

    # Tolerance for clock skew between servers (seconds)
    JWT_CLOCK_SKEW: int = env("JWT_CLOCK_SKEW", default=30, cast=int)

    # Path to RSA private key PEM file (used for signing)
    JWT_PRIVATE_KEY_PATH: str = env(
        "JWT_PRIVATE_KEY_PATH", default="keys/private.pem"
    )

    # Path to RSA public key PEM file (used for verification)
    JWT_PUBLIC_KEY_PATH: str = env(
        "JWT_PUBLIC_KEY_PATH", default="keys/public.pem"
    )

    # --------------------------------------------------------
    # Session Settings
    # --------------------------------------------------------

    # Maximum concurrent active sessions per user
    SESSION_MAX_CONCURRENT: int = env("SESSION_MAX_CONCURRENT", default=5, cast=int)

    # Inactivity timeout: 30 minutes (seconds)
    SESSION_INACTIVITY_TIMEOUT: int = env(
        "SESSION_INACTIVITY_TIMEOUT", default=60 * 30, cast=int
    )

    # Absolute session lifetime: 30 days (seconds)
    SESSION_ABSOLUTE_TTL: int = env(
        "SESSION_ABSOLUTE_TTL", default=60 * 60 * 24 * 30, cast=int
    )

    # --------------------------------------------------------
    # Password Settings
    # --------------------------------------------------------

    # Minimum password length (characters)
    PASSWORD_MIN_LENGTH: int = env("PASSWORD_MIN_LENGTH", default=12, cast=int)

    # Number of previous passwords to keep in history (cannot reuse)
    PASSWORD_HISTORY_LIMIT: int = env("PASSWORD_HISTORY_LIMIT", default=5, cast=int)

    # Argon2 parameters
    ARGON2_TIME_COST: int = env("ARGON2_TIME_COST", default=3, cast=int)
    ARGON2_MEMORY_COST: int = env("ARGON2_MEMORY_COST", default=65536, cast=int)
    ARGON2_PARALLELISM: int = env("ARGON2_PARALLELISM", default=1, cast=int)

    # --------------------------------------------------------
    # Account Lockout Policy
    # --------------------------------------------------------

    # Threshold 1: 5 failures → lock 15 minutes
    LOCKOUT_THRESHOLD_1: int = env("LOCKOUT_THRESHOLD_1", default=5, cast=int)
    LOCKOUT_DURATION_1: int = env("LOCKOUT_DURATION_1", default=60 * 15, cast=int)

    # Threshold 2: 10 failures → lock 1 hour
    LOCKOUT_THRESHOLD_2: int = env("LOCKOUT_THRESHOLD_2", default=10, cast=int)
    LOCKOUT_DURATION_2: int = env("LOCKOUT_DURATION_2", default=60 * 60, cast=int)

    # Threshold 3: 20 failures → lock 24 hours
    LOCKOUT_THRESHOLD_3: int = env("LOCKOUT_THRESHOLD_3", default=20, cast=int)
    LOCKOUT_DURATION_3: int = env(
        "LOCKOUT_DURATION_3", default=60 * 60 * 24, cast=int
    )

    # --------------------------------------------------------
    # Token Verification Lifetimes
    # --------------------------------------------------------

    # Email verification token TTL: 24 hours (seconds)
    EMAIL_VERIFY_TTL: int = env(
        "EMAIL_VERIFY_TTL", default=60 * 60 * 24, cast=int
    )

    # Password reset token TTL: 1 hour (seconds)
    PASSWORD_RESET_TTL: int = env("PASSWORD_RESET_TTL", default=60 * 60, cast=int)

    # MFA challenge token TTL: 5 minutes (seconds)
    MFA_CHALLENGE_TTL: int = env("MFA_CHALLENGE_TTL", default=60 * 5, cast=int)

    # --------------------------------------------------------
    # MFA / TOTP Settings
    # --------------------------------------------------------

    MFA_TOTP_ALGORITHM: str = "SHA1"
    MFA_TOTP_DIGITS: int = 6
    MFA_TOTP_PERIOD: int = 30   # seconds
    MFA_TOTP_VALID_WINDOW: int = 1  # ±1 step tolerance
    MFA_BACKUP_CODES_COUNT: int = 10

    # --------------------------------------------------------
    # Rate Limiting (per endpoint)
    # --------------------------------------------------------

    # Login: 10 requests per minute per IP
    RATE_LOGIN: str = env("RATE_LOGIN", default="10/minute")

    # Forgot password: 3 requests per 15 minutes per IP
    RATE_FORGOT_PASSWORD: str = env("RATE_FORGOT_PASSWORD", default="3/15minute")

    # Resend email verification: 3 per hour per user
    RATE_RESEND_VERIFICATION: str = env(
        "RATE_RESEND_VERIFICATION", default="3/hour"
    )

    # MFA verify: 5 requests per minute per user
    RATE_MFA_VERIFY: str = env("RATE_MFA_VERIFY", default="5/minute")

    # --------------------------------------------------------
    # Redis Key Namespaces
    # --------------------------------------------------------

    REDIS_REFRESH_TOKEN_PREFIX: str = "kavan:auth:refresh:"
    REDIS_BLACKLIST_PREFIX: str = "kavan:auth:blacklist:"
    REDIS_MFA_CHALLENGE_PREFIX: str = "kavan:auth:mfa_challenge:"
    REDIS_OTP_PREFIX: str = "kavan:auth:otp:"
    REDIS_RATE_LOGIN_PREFIX: str = "kavan:rate:login:"
    REDIS_RATE_FORGOT_PREFIX: str = "kavan:rate:forgot_password:"
    REDIS_LOCKOUT_PREFIX: str = "kavan:auth:lockout:"
    REDIS_SESSION_ACTIVITY_PREFIX: str = "kavan:session:activity:"
