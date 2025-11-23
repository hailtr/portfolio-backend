from backend import db
from datetime import datetime


class Education(db.Model):
    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    institution = db.Column(db.String(128))
    location = db.Column(db.String(128))
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    translations = db.relationship(
        "EducationTranslation",
        backref="education",
        cascade="all, delete-orphan",
        lazy=True,
    )
    courses = db.relationship(
        "Course", backref="education", cascade="all, delete-orphan", lazy=True
    )


class EducationTranslation(db.Model):
    __tablename__ = "education_translations"

    id = db.Column(db.Integer, primary_key=True)
    education_id = db.Column(db.Integer, db.ForeignKey("educations.id"), nullable=False)
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))  # Degree/program
    subtitle = db.Column(db.String(256))  # Field of study
    description = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint("education_id", "lang"),)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    education_id = db.Column(db.Integer, db.ForeignKey("educations.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, default=0)
