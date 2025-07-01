from datetime import datetime
from backend import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    country = db.Column(db.String(100))
    picture_url = db.Column(db.String(300))
    role = db.Column(db.String(50), default='visitor')  # 'admin', 'visitor', 'banned'
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"