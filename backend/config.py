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


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-password')

