from backend import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(32))  # Optional grouping

    def __repr__(self):
        return f"<Tag {self.name}>"
