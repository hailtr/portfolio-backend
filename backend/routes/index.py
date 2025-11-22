from flask import Blueprint, redirect

index_bp = Blueprint("public", __name__)


@index_bp.route("/")
def index():
    # Redirect root to API health check or remove this if not needed
    return redirect("/api/health")
