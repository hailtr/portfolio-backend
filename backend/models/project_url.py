from backend import db
from sqlalchemy import func


class ProjectURL(db.Model):
    """Model for storing multiple URLs per project (GitHub, Live Demo, etc.)"""
    __tablename__ = "project_urls"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, 
        db.ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    url_type = db.Column(
        db.String(32), 
        nullable=False
    )  # 'github', 'live', 'demo', 'docs', 'other'
    url = db.Column(db.String(512), nullable=False)
    label = db.Column(db.String(128))  # Optional custom label
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        db.UniqueConstraint('project_id', 'url_type', name='uq_project_url_type'),
        db.Index('idx_project_urls_project', 'project_id'),
    )
    
    def __repr__(self):
        return f"<ProjectURL {self.url_type} for Project {self.project_id}>"
    
    def to_dict(self):
        """Serialization helper for JSON responses"""
        return {
            'id': self.id,
            'type': self.url_type,
            'url': self.url,
            'label': self.label,
            'order': self.order
        }
