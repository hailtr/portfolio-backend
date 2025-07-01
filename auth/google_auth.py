import os
from flask import Blueprint, redirect, url_for, session, request, abort
from authlib.integrations.flask_client import OAuth
from backend import db
from backend.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',  # <- ¡esta es clave!
    client_kwargs={
        'scope': 'email profile'  # <- sin 'openid' para evitar validación de id_token
    }
)

@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.callback_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/google/callback')
def callback_google():
    token = google.authorize_access_token()
    if not token:
        abort(400, description="No token received")

    # Esto ahora funciona sin problemas porque `api_base_url` está definido
    resp = google.get('userinfo')
    user_info = resp.json()
    print("UserInfo:", user_info)

    if not user_info.get("verified_email"):
        return "Email not verified", 403
    
    email = user_info.get("email")
    name = user_info.get("given_name", "")
    surname = user_info.get("family_name", "")
    picture = user_info.get("picture", "")
    country = request.headers.get("X-Country", "")

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            email=email,
            name=name,
            surname=surname,
            picture_url=picture,
            country=country,
            is_verified=True,
            role="visitor",
            last_login=datetime.utcnow()
        )
        db.session.add(user)
    else:
        user.last_login = datetime.utcnow()
        user.picture_url = picture
        user.name = name
        user.surname = surname
        user.is_verified = True

    db.session.commit()


    admin_email = os.getenv("ADMIN_EMAIL")

    # Si el correo coincide con el admin, actualiza el rol en DB (aunque ya exista)
    if email == admin_email and user.role != "admin":
        print("Elevando privilegios: asignando admin")
        user.role = "admin"
        
    session['user_email'] = email
    session['user_role'] = user.role


    if user.role == "banned":
        return "Access denied", 403

    if user.role == "admin":
        return redirect(url_for("admin.admin_home", ready="true"))

    return redirect(url_for("admin.admin_home", ready="false"))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_google'))
