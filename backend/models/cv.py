"""
CV Model for PostgreSQL storage.

Stores CV data in a structured way using the existing Entity/Translation pattern.
"""

from backend import db
from datetime import datetime


class CVProfile(db.Model):
    """Main CV profile - stores personal info and settings"""

    __tablename__ = "cv_profiles"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, default="default")
    is_active = db.Column(db.Boolean, default=True)

    # Personal info (language-agnostic)
    image_url = db.Column(db.String(500))  # Online image URL
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(500))
    location_address = db.Column(db.String(255))
    location_city = db.Column(db.String(100))
    location_region = db.Column(db.String(100))
    location_country_code = db.Column(db.String(2))

    # Settings
    settings = db.Column(db.JSON)  # PDF settings, theme, etc.

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    translations = db.relationship(
        "CVTranslation", backref="profile", cascade="all, delete-orphan"
    )
    sections = db.relationship(
        "CVSection", backref="profile", cascade="all, delete-orphan"
    )

    def to_dict(self, lang="es"):
        """Convert to JSON Resume format"""
        translation = next((t for t in self.translations if t.lang == lang), None)
        if not translation and self.translations:
            translation = self.translations[0]

        if not translation:
            return {}

        # Build basics
        basics = {
            "name": translation.name,
            "label": translation.label,
            "image": self.image_url or "",
            "email": self.email or "",
            "phone": self.phone or "",
            "website": self.website or "",
            "summary": translation.summary or "",
            "location": {
                "address": self.location_address or "",
                "city": self.location_city or "",
                "region": self.location_region or "",
                "countryCode": self.location_country_code or "",
            },
        }

        # Build sections from related entities
        result = {"basics": basics}

        # Get sections ordered by display_order
        work_sections = [s.to_dict() for s in self.sections if s.section_type == "work"]
        education_sections = [
            s.to_dict() for s in self.sections if s.section_type == "education"
        ]
        skill_sections = [
            s.to_dict() for s in self.sections if s.section_type == "skill"
        ]

        if work_sections:
            result["work"] = work_sections
        if education_sections:
            result["education"] = education_sections
        if skill_sections:
            result["skills"] = skill_sections

        # Languages, interests, awards from sections
        languages = [s.to_dict() for s in self.sections if s.section_type == "language"]
        interests = [s.to_dict() for s in self.sections if s.section_type == "interest"]
        awards = [s.to_dict() for s in self.sections if s.section_type == "award"]

        if languages:
            result["languages"] = languages
        if interests:
            result["interests"] = interests
        if awards:
            result["awards"] = awards

        return result


class CVTranslation(db.Model):
    """Multilingual CV profile content"""

    __tablename__ = "cv_translations"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("cv_profiles.id"), nullable=False)
    lang = db.Column(db.String(8), nullable=False)

    name = db.Column(db.String(255))
    label = db.Column(db.String(255))  # Job title
    summary = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("profile_id", "lang", name="_cv_profile_lang_uc"),
    )


class CVSection(db.Model):
    """CV sections (work, education, skills, etc.)"""

    __tablename__ = "cv_sections"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("cv_profiles.id"), nullable=False)
    section_type = db.Column(
        db.String(32), nullable=False
    )  # 'work', 'education', 'skill', 'language', 'interest', 'award'
    display_order = db.Column(db.Integer, default=0)

    # Structured data stored as JSON
    # For work: company, position, startDate, endDate, url, summary, highlights[]
    # For education: institution, studyType, area, startDate, endDate, location, courses[]
    # For skills: name, level, keywords[]
    # etc.
    data = db.Column(db.JSON, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        """Convert section to JSON Resume format"""
        return self.data
