from flask import render_template, redirect, url_for, flash, request, Blueprint
#Contains view functions that handle HTTP requests and define URL endpoints

from flask import render_template, jsonify, redirect, url_for, flash, request, Blueprint
from rental_app import db
from rental_app.model import Client, Address, CreditCard, ClientAddress
from rental_app.clients.forms import ClientRegistrationForm, ClientLoginForm

# from rental_app.clients import clients_bp
# from rental_app.models import Manager, Car, Driver # Example of how to import models
# from rental_app.clients.forms import AddCarForm, AssignDriverForm   Example of how to import forms
clients_bp = Blueprint('clients', __name__, template_folder='templates')

@clients_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = ClientLoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(emailaddress=form.emailaddress.data).first()
        if client:
            flash('Login successful!', 'success')
            return redirect(url_for('home.homepage'))  # Or wherever you want to send them
        else:
            flash('Login failed. Email not found.', 'danger')
            return redirect(url_for('clients.login'))
    return render_template('clients_login.html', form=form)

@clients_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_client = Client.query.filter_by(emailaddress=form.emailaddress.data).first()
            if existing_client:
                flash('Email already registered. Please log in.', 'danger')
                return redirect(url_for('clients.login'))
            
            # Insert client
            new_client = Client(
                name=form.name.data,
                emailaddress=form.emailaddress.data
            )
            db.session.add(new_client)

            # Insert personal address if not exists
            personal_address = Address.query.filter_by(
                road=form.road.data,
                number=form.number.data,
                city=form.city.data
            ).first()
            if not personal_address:
                new_address = Address(
                    road=form.road.data,
                    number=form.number.data,
                    city=form.city.data
                )
                db.session.add(new_address)
                db.session.commit()

            # Insert ClientAddress
            new_client_address = ClientAddress(
                emailaddress=form.emailaddress.data,
                road=form.road.data,
                number=form.number.data,
                city=form.city.data
            )
            db.session.add(new_client_address)

            # Insert credit card address if not exists
            card_address = Address.query.filter_by(
                road=form.card_road.data,
                number=form.card_number.data,
                city=form.card_city.data
            ).first()
            if not card_address:
                new_card_address = Address(
                    road=form.card_road.data,
                    number=form.card_number.data,
                    city=form.card_city.data
                )
                db.session.add(new_card_address)
                db.session.commit()

            # Insert CreditCard
            new_creditcard = CreditCard(
                cardnumber=form.cardnumber.data,
                clientemail=form.emailaddress.data,
                road=form.card_road.data,
                number=form.card_number.data,
                city=form.card_city.data
            )
            db.session.add(new_creditcard)

            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('clients.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('clients_register.html', form=form)


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