"""
Email Alert Service

Sends email notifications for key portfolio events (CV downloads, IP bans,
new unique visitors). Uses stdlib smtplib — zero new dependencies.
Sends via background threads to avoid blocking requests.
"""

import logging
import smtplib
import threading
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

# Configuration (populated by init_alerts)
_config = {
    "enabled": False,
    "smtp_host": None,
    "smtp_port": 587,
    "smtp_user": None,
    "smtp_password": None,
    "alert_email": None,
}

# Throttle state: event_type -> last_sent_timestamp
_throttle: dict[str, float] = {}

# Throttle intervals in seconds
THROTTLE_INTERVALS = {
    "cv_download": 0,          # every occurrence
    "ip_banned": 0,            # every occurrence
    "new_unique_visitor": 600,  # max 1 per 10 minutes
}


def init_alerts(app):
    """Read SMTP config from Flask app config / env vars."""
    import os

    _config["enabled"] = os.getenv("ALERTS_ENABLED", "false").lower() == "true"
    _config["smtp_host"] = os.getenv("SMTP_HOST")
    _config["smtp_port"] = int(os.getenv("SMTP_PORT", "587"))
    _config["smtp_user"] = os.getenv("SMTP_USER")
    _config["smtp_password"] = os.getenv("SMTP_PASSWORD")
    _config["alert_email"] = os.getenv("ALERT_EMAIL") or os.getenv("ADMIN_EMAIL")

    if _config["enabled"]:
        if not _config["smtp_host"] or not _config["smtp_user"]:
            logger.warning("ALERTS_ENABLED=true but SMTP_HOST/SMTP_USER not configured — alerts will be logged only")
            _config["enabled"] = False
        else:
            logger.info(f"Email alerts enabled via {_config['smtp_host']}:{_config['smtp_port']}")
    else:
        logger.info("Email alerts disabled (ALERTS_ENABLED != true)")


def _should_send(event_type: str) -> bool:
    """Check throttle. Returns True if alert should be sent."""
    interval = THROTTLE_INTERVALS.get(event_type, 0)
    if interval == 0:
        return True
    last = _throttle.get(event_type, 0)
    return (time.time() - last) >= interval


def _record_sent(event_type: str):
    _throttle[event_type] = time.time()


def _send_email(subject: str, body_html: str):
    """Send an email in the current thread. Called from background thread."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = _config["smtp_user"]
        msg["To"] = _config["alert_email"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(_config["smtp_host"], _config["smtp_port"], timeout=10) as server:
            server.starttls()
            server.login(_config["smtp_user"], _config["smtp_password"])
            server.sendmail(_config["smtp_user"], _config["alert_email"], msg.as_string())

        logger.info(f"Alert email sent: {subject}")
    except Exception as e:
        logger.warning(f"Failed to send alert email: {e}")


def send_alert(event_type: str, **kwargs):
    """
    Public entry point. Builds the email and dispatches it in a background thread.

    Supported event_type values:
      - cv_download: ip, lang, referrer, user_agent, timestamp
      - ip_banned: ip, violation_count
      - new_unique_visitor: ip, path, referrer, user_agent
    """
    if not _should_send(event_type):
        return

    _record_sent(event_type)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    subject, body = _build_email(event_type, now, **kwargs)

    if not _config["enabled"]:
        logger.warning(f"[ALERT][{event_type}] {subject} (email disabled, logged only)")
        return

    thread = threading.Thread(target=_send_email, args=(subject, body), daemon=True)
    thread.start()


def _build_email(event_type: str, timestamp: str, **kw) -> tuple[str, str]:
    """Return (subject, html_body) for a given alert type."""

    if event_type == "cv_download":
        subject = "Portfolio Alert: CV Downloaded"
        body = f"""
        <h2>CV PDF Downloaded</h2>
        <table>
            <tr><td><b>IP</b></td><td>{kw.get('ip', 'unknown')}</td></tr>
            <tr><td><b>Language</b></td><td>{kw.get('lang', '?')}</td></tr>
            <tr><td><b>Referrer</b></td><td>{kw.get('referrer', 'direct')}</td></tr>
            <tr><td><b>User-Agent</b></td><td>{kw.get('user_agent', '?')}</td></tr>
            <tr><td><b>Time</b></td><td>{timestamp}</td></tr>
        </table>
        """

    elif event_type == "ip_banned":
        subject = f"Portfolio Alert: IP Banned — {kw.get('ip', '?')}"
        body = f"""
        <h2>IP Banned (Rate-Limit Violations)</h2>
        <table>
            <tr><td><b>IP</b></td><td>{kw.get('ip', 'unknown')}</td></tr>
            <tr><td><b>Violations</b></td><td>{kw.get('violation_count', '?')}</td></tr>
            <tr><td><b>Time</b></td><td>{timestamp}</td></tr>
        </table>
        """

    elif event_type == "new_unique_visitor":
        subject = "Portfolio Alert: New Unique Visitor"
        body = f"""
        <h2>New Unique Visitor</h2>
        <table>
            <tr><td><b>IP</b></td><td>{kw.get('ip', 'unknown')}</td></tr>
            <tr><td><b>Path</b></td><td>{kw.get('path', '/')}</td></tr>
            <tr><td><b>Referrer</b></td><td>{kw.get('referrer', 'direct')}</td></tr>
            <tr><td><b>User-Agent</b></td><td>{kw.get('user_agent', '?')}</td></tr>
            <tr><td><b>Time</b></td><td>{timestamp}</td></tr>
        </table>
        """

    else:
        subject = f"Portfolio Alert: {event_type}"
        body = f"<p>Event: {event_type}</p><p>Data: {kw}</p><p>Time: {timestamp}</p>"

    return subject, body
