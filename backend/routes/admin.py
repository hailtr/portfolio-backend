from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from sqlalchemy import text
from backend import db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from backend.services.cloudinary_service import cloudinary_service
import json
from auth.decorators import requires_login, requires_role

admin_bp = Blueprint('admin', __name__, template_folder='../../templates')


@admin_bp.route('/admin')
@requires_login
@requires_role("admin")
def admin_home():
    ready = request.args.get("ready")
    edit_id = request.args.get("edit")
    from flask import session
    print("DEBUG SESSION:", dict(session))

    if ready == "true":
        try:
            # Force reconnection check
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            
            entities = Entity.query.all()
            entity = None
            translations = {}
            available_languages = []

            if edit_id:
                entity = Entity.query.get_or_404(edit_id)
                translations = {t.lang: t for t in entity.translations}

            return render_template(
                    'admin.html',
                    entities=entities,
                    entity=entity,
                    translations=translations
                )
        
        except Exception as e:
            current_app.logger.warning(f"Error cargando entidades: {e}")
            db.session.rollback()
            return redirect(url_for('admin.admin_home', ready='false'))

    elif ready == "false":
        return render_template("admin_error.html", error="No se pudo conectar a la base de datos.")

    return render_template("admin_base.html")


@admin_bp.route('/admin/check')
def admin_check():
    retries = 3
    for attempt in range(retries):
        try:
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            return jsonify({"ready": True})
        except Exception as e:
            current_app.logger.warning(f"DB check falló (attempt {attempt + 1}/{retries}): {e}")
            db.session.rollback()
            if attempt < retries - 1:
                import time
                time.sleep(1)  # Wait 1 second before retry
    
    return jsonify({"ready": False})


@admin_bp.route('/admin/save', methods=['POST'])
def admin_save():
    form = request.form
    entity_id = form.get("id")

    if entity_id:
        entity = Entity.query.get_or_404(entity_id)
    else:
        entity = Entity()
        db.session.add(entity)

    entity.slug = form.get("slug")
    entity.type = form.get("type")
    entity.meta = {
        "category": form.get("category"),
        "tags": [t.strip() for t in form.get("tags", "").split(",") if t.strip()],
        "images": {
            "desktop": form.get("desktop_image", ""),
            "mobile": form.get("mobile_image", ""),
            "preview_video": form.get("preview_video", "")
        }
    }

    entity.translations.clear()

    # Always save ES and EN translations
    for lang in ['es', 'en']:
        try:
            content = json.loads(form.get(f"content_{lang}", '{}'))
        except json.JSONDecodeError:
            content = {}

        t = EntityTranslation(
            lang=lang,
            title=form.get(f"title_{lang}"),
            subtitle=form.get(f"subtitle_{lang}"),
            description=form.get(f"description_{lang}"),
            summary=form.get(f"summary_{lang}"),
            content=content
        )
        entity.translations.append(t)

    db.session.commit()
    return redirect(url_for('admin.admin_home', ready='true'))


@admin_bp.route('/admin/delete/<int:id>', methods=['POST'])
@requires_login
@requires_role("admin")
def admin_delete(id):
    entity = Entity.query.get_or_404(id)
    
    # Delete associated images from Cloudinary
    if entity.meta and 'images' in entity.meta:
        images = entity.meta['images']
        for img_type, img_url in images.items():
            if img_url and 'cloudinary.com' in img_url:
                public_id = cloudinary_service.extract_public_id(img_url)
                if public_id:
                    cloudinary_service.delete_image(public_id)
    
    db.session.delete(entity)
    db.session.commit()
    return redirect(url_for('admin.admin_home', ready='true'))


@admin_bp.route('/admin/upload-image', methods=['POST'])
@requires_login
@requires_role("admin")
def upload_image():
    """
    Upload an image to Cloudinary.
    
    Expects:
        - file: Image file
        - folder: Optional folder name (default: "portfolio")
        - public_id: Optional custom ID
    
    Returns:
        JSON with image URL and metadata
    """
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    # Get optional parameters
    folder = request.form.get('folder', 'portfolio')
    public_id = request.form.get('public_id')
    
    # Upload to Cloudinary
    result = cloudinary_service.upload_image(file, folder=folder, public_id=public_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@admin_bp.route('/admin/delete-image', methods=['POST'])
@requires_login
@requires_role("admin")
def delete_image():
    """
    Delete an image from Cloudinary.
    
    Expects:
        - url: Cloudinary image URL or public_id
    
    Returns:
        JSON with deletion result
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    url = data['url']
    
    # Extract public_id from URL
    public_id = cloudinary_service.extract_public_id(url)
    
    if not public_id:
        # Try using the URL as public_id directly
        public_id = url
    
    result = cloudinary_service.delete_image(public_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500
