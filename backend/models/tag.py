from backend import db
from sqlalchemy import func


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(32))  # Optional grouping
    created_at = db.Column(db.DateTime, server_default=func.now())  # Added timestamp
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())  # Added timestamp

    def __repr__(self):
        return f"<Tag {self.name}>"
