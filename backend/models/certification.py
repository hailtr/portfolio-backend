from backend import db
from datetime import datetime
from sqlalchemy import func


class Certification(db.Model):
    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    issuer = db.Column(db.String(128))
    issue_date = db.Column(db.Date, nullable=True)  # Changed from String to Date
    expiry_date = db.Column(db.Date, nullable=True)  # Changed from String to Date
    credential_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, server_default=func.now())  # Fixed deprecation
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()  # Fixed deprecation
    )

    # Relationships
    translations = db.relationship(
        "CertificationTranslation",
        backref="certification",
        cascade="all, delete-orphan",
        lazy=True,
    )
    
    def __repr__(self):
        return f"<Certification {self.slug}>"


class CertificationTranslation(db.Model):
    __tablename__ = "certification_translations"

    id = db.Column(db.Integer, primary_key=True)
    certification_id = db.Column(
        db.Integer, db.ForeignKey("certifications.id", ondelete="CASCADE"), nullable=False, index=True  # Added index and cascade
    )
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    __table_args__ = (db.UniqueConstraint("certification_id", "lang"),)
    
    def __repr__(self):
        return f"<CertificationTranslation {self.lang} for Certification {self.certification_id}>"
