from backend import db
from datetime import datetime


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    location = db.Column(db.JSON)  # {city, region, country}
    avatar_url = db.Column(db.String(256))
    social_links = db.Column(db.JSON)  # {github, linkedin, twitter, etc.}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    translations = db.relationship(
        "ProfileTranslation", backref="profile", cascade="all, delete-orphan", lazy=True
    )


class ProfileTranslation(db.Model):
    __tablename__ = "profile_translations"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    lang = db.Column(db.String(5), nullable=False)
    role = db.Column(db.String(128))  # Job title
    tagline = db.Column(db.String(256))  # Short bio
    bio = db.Column(db.Text)  # Full bio

    __table_args__ = (db.UniqueConstraint("profile_id", "lang"),)
