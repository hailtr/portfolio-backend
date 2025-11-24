from backend import db
from datetime import datetime
from sqlalchemy import func


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(64))
    # url field removed - now using urls relationship
    created_at = db.Column(db.DateTime, server_default=func.now())  # Fixed deprecation
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()  # Fixed deprecation
    )

    # Relationships
    urls = db.relationship(
        "ProjectURL", backref="project", cascade="all, delete-orphan", lazy=True, order_by="ProjectURL.order"
    )
    images = db.relationship(
        "ProjectImage", backref="project", cascade="all, delete-orphan", lazy=True
    )
    translations = db.relationship(
        "ProjectTranslation", backref="project", cascade="all, delete-orphan", lazy=True
    )
    tags = db.relationship(
        "Tag", secondary="project_tags", backref=db.backref("projects", lazy=True)
    )
    analytics = db.relationship(
        "ProjectAnalytics", backref="project", uselist=False, cascade="all, delete-orphan", lazy=True
    )
    events = db.relationship(
        "ProjectEvent", backref="project", cascade="all, delete-orphan", lazy=True
    )
    
    def __repr__(self):
        return f"<Project {self.slug}>"


class ProjectImage(db.Model):
    __tablename__ = "project_images"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    url = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(32), default="image")  # 'image', 'gif', 'video'
    
    # Enhanced metadata fields
    thumbnail_url = db.Column(db.String(512), nullable=True)
    alt_text = db.Column(db.String(256), nullable=True)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    file_size = db.Column(db.Integer, nullable=True)  # in bytes
    mime_type = db.Column(db.String(64), nullable=True)  # e.g., 'image/png', 'image/gif'
    is_featured = db.Column(db.Boolean, default=False)
    
    caption = db.Column(db.String(256))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ProjectImage {self.type} for Project {self.project_id}>"
    
    def to_dict(self):
        """Serialization helper for JSON responses"""
        return {
            'id': self.id,
            'url': self.url,
            'type': self.type,
            'thumbnail_url': self.thumbnail_url,
            'alt_text': self.alt_text,
            'width': self.width,
            'height': self.height,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_featured': self.is_featured,
            'caption': self.caption,
            'order': self.order
        }


class ProjectTranslation(db.Model):
    __tablename__ = "project_translations"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)  # Added index and cascade
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))
    subtitle = db.Column(db.String(256))
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    content = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    __table_args__ = (db.UniqueConstraint("project_id", "lang"),)
    
    def __repr__(self):
        return f"<ProjectTranslation {self.lang} for Project {self.project_id}>"


# Association table for many-to-many
project_tags = db.Table(
    "project_tags",
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),  # Added cascade
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),  # Added cascade
)
