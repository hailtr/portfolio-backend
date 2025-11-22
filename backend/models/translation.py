from backend import db


class EntityTranslation(db.Model):
    __tablename__ = "translations"

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey("entities.id"), nullable=False)
    lang = db.Column(db.String(8), nullable=False)
    title = db.Column(db.String(128))
    subtitle = db.Column(db.String(128))
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    content = db.Column(db.JSON)
