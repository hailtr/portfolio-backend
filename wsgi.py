"""
WSGI entry point for production servers.

This file is used by gunicorn, uWSGI, and other WSGI servers.
Railway and similar platforms will automatically detect this.

Usage:
    gunicorn wsgi:app
    gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
"""

import os
import sys

# Ensure imports work correctly
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from backend.app import app

# This is what the WSGI server imports
application = app

if __name__ == "__main__":
    # Fallback for direct execution
    app.run()
