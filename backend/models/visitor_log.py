from backend import db
from sqlalchemy import func


class VisitorLog(db.Model):
    """Logs every inbound request for analytics and monitoring."""
    __tablename__ = "visitor_logs"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6-sized
    path = db.Column(db.String(512), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    referrer = db.Column(db.String(512), nullable=True)
    response_time_ms = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    is_unique = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        db.Index("idx_visitor_ip_created", "ip_address", "created_at"),
    )

    def __repr__(self):
        return f"<VisitorLog {self.method} {self.path} from {self.ip_address}>"
