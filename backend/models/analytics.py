from backend import db
from sqlalchemy import func


class ProjectAnalytics(db.Model):
    """Aggregate analytics for a project"""
    __tablename__ = "project_analytics"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, 
        db.ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False, 
        unique=True,
        index=True
    )
    view_count = db.Column(db.Integer, default=0, nullable=False)
    click_count = db.Column(db.Integer, default=0, nullable=False)
    hover_count = db.Column(db.Integer, default=0, nullable=False)
    last_viewed_at = db.Column(db.DateTime, nullable=True)
    last_clicked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ProjectAnalytics for Project {self.project_id}>"
    
    def to_dict(self):
        """Serialization helper for JSON responses"""
        return {
            'project_id': self.project_id,
            'view_count': self.view_count,
            'click_count': self.click_count,
            'hover_count': self.hover_count,
            'last_viewed_at': self.last_viewed_at.isoformat() if self.last_viewed_at else None,
            'last_clicked_at': self.last_clicked_at.isoformat() if self.last_clicked_at else None
        }


class ProjectEvent(db.Model):
    """Individual analytics events for detailed tracking"""
    __tablename__ = "project_events"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, 
        db.ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    event_type = db.Column(db.String(32), nullable=False)  # 'view', 'click', 'hover'
    session_id = db.Column(db.String(128), nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 max length
    referrer = db.Column(db.String(512), nullable=True)
    event_data = db.Column(db.JSON, nullable=True)  # Additional event data (renamed from 'metadata')
    created_at = db.Column(db.DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        db.Index('idx_project_events_type', 'project_id', 'event_type'),
        db.Index('idx_project_events_created', 'created_at'),
    )

    def __repr__(self):
        return f"<ProjectEvent {self.event_type} for Project {self.project_id}>"
    
    def to_dict(self):
        """Serialization helper for JSON responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'event_type': self.event_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'event_data': self.event_data
        }
