from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from sqlalchemy import text
from backend import db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
import json

admin_bp = Blueprint('admin', __name__, template_folder='../../templates')


@admin_bp.route('/admin')
def admin_home():
    ready = request.args.get("ready")
    edit_id = request.args.get("edit")

    if ready == "true":
        try:
            entities = Entity.query.all()
            entity = None
            translations = {}
            available_languages = []

            

            if edit_id:
                entity = Entity.query.get_or_404(edit_id)
                translations = {t.lang: t for t in entity.translations}
                available_languages = list(translations.keys())
            
            if not available_languages:
                available_languages = ['es', 'en']

            return render_template(
                    'admin.html',
                    entities=entities,
                    entity=entity,
                    translations=translations,
                    available_languages=available_languages
                )
        
        except Exception as e:
            current_app.logger.warning(f"Error cargando entidades: {e}")
            return redirect(url_for('admin.admin_home', ready='false'))

    elif ready == "false":
        return render_template("admin_error.html", error="No se pudo conectar a la base de datos.")

    return render_template("admin_base.html")


@admin_bp.route('/admin/check')
def admin_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"ready": True})
    except Exception as e:
        current_app.logger.warning(f"DB check falló: {e}")
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
        "tags": [t.strip() for t in form.get("tags", "").split(",") if t.strip()]
    }

    entity.translations.clear()

    langs = [k.split("_")[1] for k in form if k.startswith("lang_")]
    for lang in langs:
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
def admin_delete(id):
    entity = Entity.query.get_or_404(id)
    db.session.delete(entity)
    db.session.commit()
    return redirect(url_for('admin.admin_home', ready='true'))
