from backend import db
from datetime import datetime


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    company = db.Column(db.String(128))
    location = db.Column(db.String(128))
    start_date = db.Column(db.String(32))  # e.g., "2020-01" or "Jan 2020"
    end_date = db.Column(db.String(32))
    current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    translations = db.relationship(
        "ExperienceTranslation",
        backref="experience",
        cascade="all, delete-orphan",
        lazy=True,
    )
    tags = db.relationship(
        "Tag", secondary="experience_tags", backref=db.backref("experiences", lazy=True)
    )


class ExperienceTranslation(db.Model):
    __tablename__ = "experience_translations"

    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(
        db.Integer, db.ForeignKey("experiences.id"), nullable=False
    )
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))  # Job title/role
    subtitle = db.Column(db.String(256))
    description = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("experience_id", "lang"),)


# Association table
experience_tags = db.Table(
    "experience_tags",
    db.Column(
        "experience_id", db.Integer, db.ForeignKey("experiences.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)
