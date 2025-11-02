from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app

index_bp = Blueprint('public',__name__, template_folder='../../templates')

@index_bp.route('/')
def index():
    return render_template('base.html')