from backend import db
from datetime import datetime
from sqlalchemy import func


class SkillCategory(db.Model):
    __tablename__ = "skill_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    order = db.Column(db.Integer, default=0)
    
    # Relationships
    translations = db.relationship(
        "SkillCategoryTranslation", backref="category", cascade="all, delete-orphan", lazy=True
    )
    skills = db.relationship(
        "Skill", backref="skill_category", lazy=True
    )

    def __repr__(self):
        return f"<SkillCategory {self.slug}>"


class SkillCategoryTranslation(db.Model):
    __tablename__ = "skill_category_translations"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("skill_categories.id", ondelete="CASCADE"), nullable=False)
    lang = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    __table_args__ = (db.UniqueConstraint("category_id", "lang"),)

    def __repr__(self):
        return f"<SkillCategoryTranslation {self.lang} for {self.category_id}>"


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    icon_url = db.Column(db.String(256))
    proficiency = db.Column(db.Integer, default=50)  # 0-100
    
    # New fields
    category_id = db.Column(db.Integer, db.ForeignKey("skill_categories.id"), nullable=True) # Nullable for migration
    is_visible_cv = db.Column(db.Boolean, default=True)
    is_visible_portfolio = db.Column(db.Boolean, default=True)
    
    # Deprecated (keep for migration)
    category = db.Column(db.String(64))  
    
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()
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
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    lang = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(128), nullable=False)  # Display name
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (db.UniqueConstraint("skill_id", "lang"),)
    
    def __repr__(self):
        return f"<SkillTranslation {self.lang} for Skill {self.skill_id}>"
