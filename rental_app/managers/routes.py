from flask import render_template, redirect, url_for, flash, request, Blueprint
from rental_app import db
# from rental_app.managers import managers_bp
# from rental_app.models import Manager, Car, Driver # Example of how to import models
# from rental_app.managers.forms import AddCarForm, AssignDriverForm   Example of how to import forms


managers_bp = Blueprint('managers', __name__, template_folder='templates')