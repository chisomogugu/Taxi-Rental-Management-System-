# app/managers/__init__.py
from flask import Blueprint
from rental_app.managers import routes

managers_bp = Blueprint('managers', __name__, template_folder='templates')
