from backend import db
from datetime import datetime


class Certification(db.Model):
    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    issuer = db.Column(db.String(128))
    issue_date = db.Column(db.String(32))
    expiry_date = db.Column(db.String(32))
    credential_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    translations = db.relationship(
        "CertificationTranslation",
        backref="certification",
        cascade="all, delete-orphan",
        lazy=True,
    )


class CertificationTranslation(db.Model):
    __tablename__ = "certification_translations"

    id = db.Column(db.Integer, primary_key=True)
    certification_id = db.Column(
        db.Integer, db.ForeignKey("certifications.id"), nullable=False
    )
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("certification_id", "lang"),)
