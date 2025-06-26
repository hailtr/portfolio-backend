from flask import Blueprint, render_template, request, redirect, url_for
from backend import db
from backend.models.entity import Entity
import json

admin_bp = Blueprint('admin', __name__, template_folder='../../templates')

@admin_bp.route('/admin')
def admin_home():
    slug = request.args.get("slug", "portfolio")
    entity = Entity.query.filter_by(slug=slug).first_or_404()

    # Load translations for the entity
    translations = {t.lang: t for t in entity.translations}

    # Load available languages
    languages = [t.lang for t in entity.translations]


    return render_template(
        'admin.html',
        entity=entity,
        translations=translations,
        languages=languages
    )


@admin_bp.route('/admin/create', methods=['POST'])
def admin_create():
    slug = request.form['slug']
    type_ = request.form['type']
    category = request.form['category']
    tags = request.form.get('tags', '').split(',')

    meta = {
        "category": category,
        "tags": [t.strip() for t in tags if t.strip()],
        "images": {}
    }

    entity = Entity(slug=slug, type=type_, meta=meta)
    db.session.add(entity)
    db.session.commit()
    return redirect(url_for('admin.admin_home'))

@admin_bp.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete(id):
    entity = Entity.query.get(id)
    if entity:
        db.session.delete(entity)
        db.session.commit()
    return redirect(url_for('admin.admin_home'))
