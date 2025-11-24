from backend import db
from datetime import datetime
from sqlalchemy import func


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    icon_url = db.Column(db.String(256))
    proficiency = db.Column(db.Integer, default=50)  # 0-100
    category = db.Column(db.String(64))  # e.g., "programming", "tools", "languages"
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Fixed deprecation
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()  # Fixed deprecation
    )

    # Relationships
    translations = db.relationship(
        "SkillTranslation", backref="skill", cascade="all, delete-orphan", lazy=True
    )
    
    def __repr__(self):
        return f"<Skill {self.slug}>"


class SkillTranslation(db.Model):
    __tablename__ = "skill_translations"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)  # Added index and cascade
    lang = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(128), nullable=False)  # Display name
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    __table_args__ = (db.UniqueConstraint("skill_id", "lang"),)
    
    def __repr__(self):
        return f"<SkillTranslation {self.lang} for Skill {self.skill_id}>"
