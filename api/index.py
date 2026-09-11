"""
Vercel Serverless Entry Point
-----------------------------
Vercel's Python runtime looks for an `app` variable (WSGI/ASGI callable)
in api/index.py.  This file bootstraps the Flask application from the
backend package and exposes it for Vercel.
"""

import os
import sys

# Add the backend directory to sys.path so that existing imports
# (config, extensions, models, routes.*) resolve without changes.
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend')
backend_dir = os.path.normpath(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app, initialize_database  # noqa: E402

app = create_app()

# Initialize database tables + seed data on cold start.
# In serverless, this runs once per container lifecycle.
initialize_database(app)
