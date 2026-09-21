import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
load_dotenv()  # also check current working dir


def _resolve_database_uri():
    """Return the database URI, preferring Vercel Postgres env vars."""
    # Vercel injects POSTGRES_URL when you provision a Postgres database.
    # Some providers use DATABASE_URL instead — check both.
    uri = os.getenv('POSTGRES_URL') or os.getenv('DATABASE_URL')
    if uri:
        # Vercel/Neon sometimes provide postgres:// which SQLAlchemy 2.x
        # does not accept — it requires postgresql://
        if uri.startswith('postgres://'):
            uri = uri.replace('postgres://', 'postgresql://', 1)
        return uri
    # Local development fallback
    return 'sqlite:///database.db'


def _is_production():
    """Return True when running in a production environment."""
    return bool(os.getenv('VERCEL') or os.getenv('PRODUCTION'))


class Config:
    # --- Security ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Fail loudly in production if SECRET_KEY is not set
    if _is_production() and SECRET_KEY == 'dev-secret-key-change-in-production':
        raise RuntimeError(
            'SECRET_KEY environment variable must be set in production. '
            'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
        )

    # --- Database ---
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,      # Reconnect stale connections (serverless)
        'pool_recycle': 300,         # Recycle connections every 5 min
    }

    # --- Uploads ---
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # --- S3 (production image uploads) ---
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    USE_S3 = bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_S3_BUCKET)

    # --- Admin ---
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-password')

    # --- Session / Cookies ---
    SESSION_COOKIE_SECURE = _is_production()
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
