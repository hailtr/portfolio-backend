from backend import db
from datetime import datetime


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(64))
    url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    images = db.relationship(
        "ProjectImage", backref="project", cascade="all, delete-orphan", lazy=True
    )
    translations = db.relationship(
        "ProjectTranslation", backref="project", cascade="all, delete-orphan", lazy=True
    )
    tags = db.relationship(
        "Tag", secondary="project_tags", backref=db.backref("projects", lazy=True)
    )


class ProjectImage(db.Model):
    __tablename__ = "project_images"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(32), default="image")  # 'image' or 'gif'
    caption = db.Column(db.String(256))
    order = db.Column(db.Integer, default=0)


class ProjectTranslation(db.Model):
    __tablename__ = "project_translations"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))
    subtitle = db.Column(db.String(256))
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    content = db.Column(db.JSON)

    __table_args__ = (db.UniqueConstraint("project_id", "lang"),)


# Association table for many-to-many
project_tags = db.Table(
    "project_tags",
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)
