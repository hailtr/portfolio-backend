from backend import db
from datetime import datetime
from sqlalchemy import func


class Education(db.Model):
    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    institution = db.Column(db.String(128))
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
        "EducationTranslation",
        backref="education",
        cascade="all, delete-orphan",
        lazy=True,
    )
    courses = db.relationship(
        "Course", backref="education", cascade="all, delete-orphan", lazy=True
    )
    
    def __repr__(self):
        return f"<Education {self.slug}>"


class EducationTranslation(db.Model):
    __tablename__ = "education_translations"

    id = db.Column(db.Integer, primary_key=True)
    education_id = db.Column(db.Integer, db.ForeignKey("educations.id", ondelete="CASCADE"), nullable=False, index=True)  # Added index and cascade
    lang = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(128))  # Degree/program
    subtitle = db.Column(db.String(256))  # Field of study
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    __table_args__ = (db.UniqueConstraint("education_id", "lang"),)
    
    def __repr__(self):
        return f"<EducationTranslation {self.lang} for Education {self.education_id}>"


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    education_id = db.Column(db.Integer, db.ForeignKey("educations.id", ondelete="CASCADE"), nullable=False, index=True)  # Added index and cascade
    name = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp
    
    def __repr__(self):
        return f"<Course {self.name}>"
    
    def to_dict(self):
        """Serialization helper for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order
        }
