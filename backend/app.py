import os
import logging
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from backend import db
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from backend.routes.admin import admin_bp
from backend.routes.api import api_bp
from backend.routes.cv import cv_bp
from auth.google_auth import auth_bp, oauth
from backend.routes.index import index_bp
from backend.services.cache_service import cache, check_cache_health
from backend.utils import rate_limit

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

logger.info("Starting Flask application")

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for frontend access
# In production, restrict origins to your Vercel domain
default_origins = (
    "http://localhost:3000,http://localhost:5173,https://rfo-portfolio.vercel.app"
)
cors_origins = os.getenv("CORS_ORIGINS", default_origins).split(",")
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False,
        }
    },
)

# App configuration
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_super_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///portfolio.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ADMIN_TOKEN"] = os.getenv("ADMIN_TOKEN", "changeme")

# Session configuration
from datetime import timedelta

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)  # Session lasts 7 days
# Secure cookies in production (HTTPS), False for local development
app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,  # Recycle connections before Railway's 5min timeout
    "pool_size": 10,
    "max_overflow": 20,
    "connect_args": {
        "connect_timeout": 10,  # Increased timeout
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
}

oauth.init_app(app)

logger.info("Database URI loaded from environment")
db.init_app(app)
logger.info("Database connection initialized")

# Initialize cache
cache.init_app(app)
logger.info("Cache initialized")

# Initialize compression (gzip responses)
compress = Compress(app)
logger.info("Response compression enabled")

# Initialize rate limiter
# Storage: Use Redis if available, otherwise in-memory
redis_url = os.getenv("REDIS_URL")
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=redis_url if redis_url else "memory://",
    default_limits=["200 per day", "50 per hour"],  # Global limits
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",
)
logger.info(
    f"Rate limiter initialized with {'Redis' if redis_url else 'memory'} storage"
)

# Make limiter available to routes
rate_limit.init_limiter(limiter)

logger.info("Registering blueprints")
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)
app.register_blueprint(cv_bp)


# Enhanced health check endpoint
@app.route("/health", methods=["GET"])
def health():
    """Comprehensive health check including cache and database"""
    health_status = {"status": "healthy", "timestamp": time.time(), "services": {}}

    # Check database
    try:
        db.session.execute(text("SELECT 1"))
        health_status["services"]["database"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = f"error: {str(e)}"

    # Check cache
    cache_healthy = check_cache_health()
    health_status["services"]["cache"] = (
        "operational" if cache_healthy else "unavailable"
    )

    # Check rate limiter
    health_status["services"]["rate_limiter"] = "active"
    health_status["services"]["cache_type"] = "redis" if redis_url else "memory"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code


# Run the app
if __name__ == "__main__":
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
                logger.warning(
                    f"Connection failed: (attempt {retries}), retrying in {wait_time}s..."
                )
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
