"""
Vercel Serverless Entry Point
-----------------------------
Vercel's Python runtime looks for an `app` variable (WSGI/ASGI callable)
in api/index.py.  This file bootstraps the Flask application from the
backend package and exposes it for Vercel.
"""

import os
import sys
import traceback

# Add both the project root and backend directory to sys.path so that
# all module references resolve reliably in serverless environments.
root_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
backend_dir = os.path.normpath(os.path.join(root_dir, 'backend'))

for path in (root_dir, backend_dir):
    if path not in sys.path:
        sys.path.insert(0, path)

from app import create_app, initialize_database  # noqa: E402

app = create_app()

# Initialize database tables + seed data on cold start.
# In serverless, this runs once per container lifecycle.
try:
    initialize_database(app)
except Exception as e:
    traceback.print_exc(file=sys.stderr)
    print(f"[ERROR] initialize_database failed: {e}", file=sys.stderr, flush=True)

