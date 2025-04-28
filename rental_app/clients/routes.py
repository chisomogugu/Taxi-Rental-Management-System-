#Contains view functions that handle HTTP requests and define URL endpoints

from flask import render_template, jsonify, redirect, url_for, flash, request, Blueprint
from rental_app import db
# from rental_app.clients import clients_bp
# from rental_app.models import Manager, Car, Driver # Example of how to import models
# from rental_app.clients.forms import AddCarForm, AssignDriverForm   Example of how to import forms
clients_bp = Blueprint('clients', __name__, template_folder='templates')

@clients_bp.route('/dashboard', methods = ['GET'])
def dashboard():
    return render_template('index.html')

# Fetch cars by brands from the database sql
# @clients_bp.route('/inventory/<brand>')
# def inventory(brand):
#     conn = sqlite3.connect('your_database.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT Model.modelid
#         FROM Model
#         JOIN Car ON Model.modelid = Car.carid
#         WHERE Car.brand = ?
#     """, (brand,))
#     models = [row[0] for row in cursor.fetchall()]
#     conn.close()
#     return jsonify(models=models)

#Temporary testing data
@clients_bp.route('/inventory/<brand>')
def inventory(brand):
    # Temporary fake inventory data
    models = []

    if brand.lower() == 'kia':
        models = ['K5', 'Sorento', 'Sportage']
    elif brand.lower() == 'toyota':
        models = ['Corolla', 'Camry', 'RAV4']
    elif brand.lower() == 'bmw':
        models = ['3 Series', 'X5', 'M4']
    elif brand.lower() == 'audi':
        models = ['A4', 'Q5', 'A6']
    elif brand.lower() == 'maercedes': 
        models = ['GLE', 'C-Class', 'E-Class']
    elif brand.lower() == 'tesla':
        models = ['Model 3', 'Model S', 'Model X']
    elif brand.lower() == 'range rover':
        models = ['Evoque', 'Velar', 'Sport']
    elif brand.lower() == 'jeep':
        models = ['Wrangler', 'Grand Cherokee', 'Compass']
    elif brand.lower() == 'volkswagen':
        models = ['Golf', 'Passat', 'Tiguan']
    else:
        models = ['No inventory found']

    return jsonify(models=models)