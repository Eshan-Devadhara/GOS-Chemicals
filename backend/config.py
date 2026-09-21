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
    # Vercel read-only filesystem fallback uses /tmp
    if os.getenv('VERCEL'):
        db_dir = os.path.abspath('/tmp/gos_chemicals_instance')
        try:
            os.makedirs(db_dir, exist_ok=True)
        except OSError:
            pass
        db_path = os.path.join(db_dir, 'database.db').replace(os.sep, '/')
        return f'sqlite:///{db_path}'
    # Local development fallback
    return 'sqlite:///database.db'


def _is_production():
    """Return True when running in a production environment."""
    return bool(os.getenv('PRODUCTION'))


class Config:
    # --- Security ---
    # See below for production secrets

    # --- Database ---
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,      # Reconnect stale connections (serverless)
        'pool_recycle': 300,         # Recycle connections every 5 min
    }

    # --- Uploads ---
    if os.getenv('VERCEL'):
        UPLOAD_FOLDER = os.path.join(os.path.abspath('/tmp/gos_chemicals_instance'), 'uploads')
    else:
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # --- Cloudinary (production image uploads) ---
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    USE_CLOUDINARY = bool(CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)

    if _is_production():
        SECRET_KEY = os.getenv('SECRET_KEY')
        if not SECRET_KEY or SECRET_KEY == 'dev-secret-key-change-in-production':
            raise RuntimeError("SECRET_KEY environment variable must be set in production.")
            
        ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
        if not ADMIN_EMAIL or ADMIN_EMAIL == 'admin@example.com':
            raise RuntimeError("ADMIN_EMAIL environment variable must be set in production.")
            
        ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
        if not ADMIN_PASSWORD or ADMIN_PASSWORD == 'change-this-password':
            raise RuntimeError("ADMIN_PASSWORD environment variable must be set to a strong password in production.")
    else:
        SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-password')

    # --- Session / Cookies ---
    SESSION_COOKIE_SECURE = bool(os.getenv('VERCEL') or os.getenv('PRODUCTION'))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
