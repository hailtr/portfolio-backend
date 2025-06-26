from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from backend import db

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_TOKEN'] = os.getenv("ADMIN_TOKEN", "changeme")

db.init_app(app)

# Importar modelos para registrar
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation


# Middleware auth simple
@app.before_request
def check_token():
    if request.method in ['POST', 'PUT', 'DELETE'] and request.path.startswith('/api/'):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token != app.config['ADMIN_TOKEN']:
            abort(401)

# Endpoint principal de lectura
@app.route('/api/portfolio')
def get_portfolio():
    lang = request.args.get('lang', 'es')
    out = {
        "projects": [], "profile": None, "about": None,
        "experience": [], "education": [], "footer": None, "cards": [], "ui": {}
    }
    
    entities = Entity.query.all()
    for e in entities:
        t = next((tr for tr in e.translations if tr.lang == lang), None)
        if not t: continue

        obj = {
            "id": e.slug,
            "title": t.title,
            "subtitle": t.subtitle,
            "description": t.description,
            "summary": t.summary,
            "content": t.content,
            "meta": e.meta
        }

        if e.type == "project": out["projects"].append(obj)
        elif e.type == "profile": out["profile"] = obj
        elif e.type == "about": out["about"] = obj
        elif e.type == "experience": out["experience"].append(obj)
        elif e.type == "education": out["education"].append(obj)
        elif e.type == "footer": out["footer"] = obj
        elif e.type == "card": out["cards"].append(obj)
        elif e.type == "ui": out["ui"] = obj.get("content", {})

    return jsonify(out)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
