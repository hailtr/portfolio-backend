"""
Bot Detection Middleware

Blocks requests with empty/missing User-Agent or known malicious bot UAs.
Skips health endpoints so uptime monitors can still reach them.
"""

import logging
from flask import request, jsonify

logger = logging.getLogger(__name__)

# Substrings matched case-insensitively against User-Agent
BLOCKED_UA_PATTERNS = [
    "scrapy",
    "python-requests",
    "python-urllib",
    "go-http-client",
    "java/",
    "libwww-perl",
    "wget",
    "httpie",
    "httpclient",
    "aiohttp",
    "node-fetch",
    "php/",
    "masscan",
    "nikto",
    "sqlmap",
    "nmap",
    "zgrab",
    "censys",
    "shodan",
]

EXEMPT_PATHS = {"/health", "/api/health"}


def register_bot_filter(app):
    """Register the bot-detection before_request hook."""

    @app.before_request
    def block_bots():
        if request.path in EXEMPT_PATHS:
            return None

        ua = request.headers.get("User-Agent", "").strip()

        if not ua:
            logger.warning(f"Blocked request with empty User-Agent from {request.remote_addr}")
            return jsonify({"error": True, "message": "Forbidden", "status": 403}), 403

        ua_lower = ua.lower()
        for pattern in BLOCKED_UA_PATTERNS:
            if pattern in ua_lower:
                logger.warning(
                    f"Blocked bot UA '{ua}' (matched '{pattern}') from {request.remote_addr}"
                )
                return jsonify({"error": True, "message": "Forbidden", "status": 403}), 403

        return None
