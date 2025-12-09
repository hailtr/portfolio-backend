web: alembic upgrade head && gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --graceful-timeout 90 --log-level info
