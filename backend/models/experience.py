from backend import db
from datetime import datetime
from sqlalchemy import func


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    company = db.Column(db.String(128))
    location = db.Column(db.String(128))
    start_date = db.Column(db.Date, nullable=True)  # Changed from String to Date
    end_date = db.Column(db.Date, nullable=True)  # Changed from String to Date
    current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Fixed deprecation
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()  # Fixed deprecation
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
    
    def __repr__(self):
        return f"<Experience {self.slug}>"


class ExperienceTranslation(db.Model):
    __tablename__ = "experience_translations"

    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(
        db.Integer, db.ForeignKey("experiences.id", ondelete="CASCADE"), nullable=False, index=True  # Added index and cascade
    )
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))  # Job title/role
    subtitle = db.Column(db.String(256))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    __table_args__ = (db.UniqueConstraint("experience_id", "lang"),)
    
    def __repr__(self):
        return f"<ExperienceTranslation {self.lang} for Experience {self.experience_id}>"


# Association table
experience_tags = db.Table(
    "experience_tags",
    db.Column(
        "experience_id", db.Integer, db.ForeignKey("experiences.id", ondelete="CASCADE"), primary_key=True  # Added cascade
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),  # Added cascade
)
