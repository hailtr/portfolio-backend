#!/usr/bin/env python
"""
Usage:
    Development:  python run.py
    Production:   gunicorn run:app
    Railway:      Automatically detected
"""

import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from backend.app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

