"""
Request Logger Middleware

Logs every request to the visitor_logs table for analytics.
Skips static files, health endpoints, and admin assets.
Determines uniqueness via an in-memory IP+UA set (reset daily).
"""

import logging
import threading
import time
from datetime import date

from flask import g, request

logger = logging.getLogger(__name__)

# In-memory set of (ip, ua) for uniqueness check. Reset daily.
_seen_lock = threading.Lock()
_seen_combos: set[tuple[str, str]] = set()
_seen_date: date = date.today()

# Paths to skip logging
SKIP_PREFIXES = ("/static/", "/favicon")
SKIP_EXACT = {"/health", "/api/health"}


def _reset_if_new_day():
    """Reset the seen-combos set at the start of each new day. Caller must hold _seen_lock."""
    global _seen_combos, _seen_date
    today = date.today()
    if today != _seen_date:
        _seen_combos = set()
        _seen_date = today


def register_request_logger(app):
    """Register before/after request hooks for visitor logging."""

    @app.before_request
    def _start_timer():
        g.start_time = time.time()

    @app.after_request
    def _log_request(response):
        # Skip paths we don't want to track
        path = request.path
        if path in SKIP_EXACT:
            return response
        for prefix in SKIP_PREFIXES:
            if path.startswith(prefix):
                return response

        try:
            ip = request.remote_addr or "0.0.0.0"
            ua = (request.user_agent.string or "")[:512]
            combo = (ip, ua)

            with _seen_lock:
                _reset_if_new_day()
                is_unique = combo not in _seen_combos
                if is_unique:
                    _seen_combos.add(combo)

            elapsed_ms = None
            start = getattr(g, "start_time", None)
            if start:
                elapsed_ms = int((time.time() - start) * 1000)

            from backend import db
            from backend.models.visitor_log import VisitorLog

            log_entry = VisitorLog(
                ip_address=ip,
                path=path[:512],
                method=request.method,
                status_code=response.status_code,
                user_agent=ua,
                referrer=(request.referrer or "")[:512] or None,
                response_time_ms=elapsed_ms,
                is_unique=is_unique,
            )
            db.session.add(log_entry)
            db.session.commit()

            # Trigger unique-visitor alert
            if is_unique:
                from backend.services.alert_service import send_alert

                send_alert(
                    "new_unique_visitor",
                    ip=ip,
                    path=path,
                    referrer=request.referrer or "direct",
                    user_agent=ua,
                )

        except Exception as e:
            logger.warning(f"Request logger failed: {e}")
            try:
                from backend import db
                db.session.rollback()
            except Exception:
                pass

        return response
