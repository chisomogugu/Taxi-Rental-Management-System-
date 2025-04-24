"""
Contains view functions that handle HTTP requests and define URL endpoints
"""

from flask import render_template, redirect, url_for, flash, request, Blueprint
from rental_app import db
# from rental_app.models import Manager, Car, Driver # Example of how to import models
# from rental_app.home.forms import AddCarForm, AssignDriverForm   Example of how to import forms

home_bp = Blueprint('home', __name__, template_folder='templates')


