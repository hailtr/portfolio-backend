from flask import Blueprint, render_template, request, redirect, url_for
from backend import db
from backend.models.entity import Entity
import json

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

@admin_bp.route('/admin')
def admin_home():
    projects = Entity.query.filter_by(type="project").all()
    return render_template('admin.html', projects=projects)

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
