import os
import logging
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from backend import db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

logger.info("Starting Flask application")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_TOKEN'] = os.getenv("ADMIN_TOKEN", "changeme")

logger.info("Database URI loaded from environment")
db.init_app(app)
logger.info("Database connection initialized")

# Simple admin token middleware for protected routes
@app.before_request
def check_token():
    if request.method in ['POST', 'PUT', 'DELETE'] and request.path.startswith('/api/'):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token != app.config['ADMIN_TOKEN']:
            logger.warning("Unauthorized access attempt")
            abort(401)

# Public portfolio endpoint
@app.route('/api/portfolio')
def get_portfolio():
    lang = request.args.get('lang', 'es')
    logger.info(f"Public request received: lang={lang}")

    out = {
        "projects": [], "profile": None, "about": None,
        "experience": [], "education": [], "footer": None, "cards": [], "ui": {}
    }
    
    entities = Entity.query.all()
    logger.info(f"Found {len(entities)} entities in total")

    for e in entities:
        # Find translation for requested language
        t = next((tr for tr in e.translations if tr.lang == lang), None)
        if not t:
            logger.debug(f"[{e.slug}] No translation in '{lang}', skipping.")
            continue

        obj = {
            "id": e.slug,
            "title": t.title,
            "subtitle": t.subtitle,
            "description": t.description,
            "summary": t.summary,
            "content": t.content,
            "meta": e.meta
        }

        # Group content by entity type
        if e.type == "project": out["projects"].append(obj)
        elif e.type == "profile": out["profile"] = obj
        elif e.type == "about": out["about"] = obj
        elif e.type == "experience": out["experience"].append(obj)
        elif e.type == "education": out["education"].append(obj)
        elif e.type == "footer": out["footer"] = obj
        elif e.type == "card": out["cards"].append(obj)
        elif e.type == "ui": out["ui"] = obj.get("content", {})

    logger.info("Response successfully generated")
    return jsonify(out)

# Run the app
if __name__ == '__main__':
    logger.info("Running app as standalone script")
    with app.app_context():
        logger.info("Creating tables if not exist...")
        db.create_all()
        logger.info("Database tables ready")
    logger.info("Starting server in debug mode")
    app.run(debug=True)
