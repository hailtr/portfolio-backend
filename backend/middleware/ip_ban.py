"""
IP Ban Middleware

Tracks IPs that receive 429 responses. After 5 violations within 10 minutes,
the IP is blocked for 30 minutes. Uses in-memory storage with TTL-based expiry.
"""

import logging
import time
from flask import request, jsonify

logger = logging.getLogger(__name__)

VIOLATION_WINDOW = 600  # 10 minutes
BAN_DURATION = 1800  # 30 minutes
MAX_VIOLATIONS = 5

EXEMPT_PATHS = {"/health", "/api/health"}

# ip -> list of violation timestamps
_violations: dict[str, list[float]] = {}
# ip -> ban expiry timestamp
_bans: dict[str, float] = {}


def _cleanup():
    """Remove expired entries to prevent memory growth."""
    now = time.time()
    expired_bans = [ip for ip, exp in _bans.items() if exp <= now]
    for ip in expired_bans:
        del _bans[ip]
        _violations.pop(ip, None)

    cutoff = now - VIOLATION_WINDOW
    expired_violations = []
    for ip, timestamps in _violations.items():
        _violations[ip] = [t for t in timestamps if t > cutoff]
        if not _violations[ip]:
            expired_violations.append(ip)
    for ip in expired_violations:
        del _violations[ip]


def record_violation(ip: str):
    """Record a rate-limit violation for an IP. Called from the 429 handler."""
    now = time.time()
    cutoff = now - VIOLATION_WINDOW

    if ip not in _violations:
        _violations[ip] = []

    _violations[ip] = [t for t in _violations[ip] if t > cutoff]
    _violations[ip].append(now)

    if len(_violations[ip]) >= MAX_VIOLATIONS:
        _bans[ip] = now + BAN_DURATION
        logger.warning(f"IP {ip} banned for {BAN_DURATION}s after {len(_violations[ip])} rate-limit violations")
        try:
            from backend.services.alert_service import send_alert
            send_alert("ip_banned", ip=ip, violation_count=len(_violations[ip]))
        except Exception:
            pass


def register_ip_ban(app):
    """Register the IP-ban before_request hook."""

    @app.before_request
    def check_ip_ban():
        if request.path in EXEMPT_PATHS:
            return None

        now = time.time()
        ip = request.remote_addr

        # Periodic cleanup (roughly every 100 requests via simple modulo on dict size)
        if len(_bans) + len(_violations) > 100:
            _cleanup()

        ban_expiry = _bans.get(ip)
        if ban_expiry:
            if now < ban_expiry:
                remaining = int(ban_expiry - now)
                logger.info(f"Blocked banned IP {ip} ({remaining}s remaining)")
                return jsonify({
                    "error": True,
                    "message": "Temporarily blocked",
                    "status": 403,
                }), 403
            else:
                # Ban expired
                del _bans[ip]
                _violations.pop(ip, None)

        return None
