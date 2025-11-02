import os
import logging
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from backend import db
import time
from sqlalchemy.exc import OperationalError
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from sqlalchemy import text
from backend.routes.admin import admin_bp
from backend.routes.api import api_bp
from auth.google_auth import auth_bp, oauth
from backend.routes.index import index_bp

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

# Configure CORS for frontend access
# In production, restrict origins to your Vercel domain
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# App configuration
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_super_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_TOKEN'] = os.getenv("ADMIN_TOKEN", "changeme")

# Session configuration
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts 7 days
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,  # Recycle connections before Railway's 5min timeout
    "pool_size": 10,
    "max_overflow": 20,
    "connect_args": {
        "connect_timeout": 10,  # Increased timeout
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
}

oauth.init_app(app)

logger.info("Database URI loaded from environment")
db.init_app(app)
logger.info("Database connection initialized")

logger.info("Registering blueprints")
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)


# Run the app
if __name__ == '__main__':
    logger.info("Running app as standalone script")

    with app.app_context():
        retries = 0
        while retries < 10:
            try:
                logger.info("Trying to connect to the database...")
                db.session.execute(text("SELECT 1"))
                logger.info("Database connection successful")
                break
            except OperationalError as e:
                retries += 1
                wait_time = 0 + retries
                logger.warning(f"Connection failed: (attempt {retries}), retrying in {wait_time}s...")
                time.sleep(wait_time)
        else:
            logger.error("Database connection failed after multiple retries")
            exit(1)

        logger.info("Creating tables if not exist...")
        db.create_all()
        logger.info("Database tables ready")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route registered: {rule.endpoint} -> {rule}")
    logger.info("Starting server in debug mode")
    app.run(debug=True)