from flask import render_template, redirect, jsonify, url_for, flash, session, request, Blueprint
from rental_app import db
from rental_app.model import Client, Address, CreditCard, ClientAddress, Car, Model, Rent
from rental_app.clients.forms import ClientRegistrationForm, ClientLoginForm

#Contains view functions that handle HTTP requests and define URL endpoints
clients_bp = Blueprint('clients', __name__, template_folder='templates')

@clients_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = ClientLoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(emailaddress=form.emailaddress.data).first()
        if client:
            session['client_email'] = client.emailaddress   # <-- Save client email in session
            flash('Login successful!', 'success')
            return redirect(url_for('clients.dashboard'))
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


@clients_bp.route('/dashboard', methods=['GET'])
def dashboard():
    client_email = session.get('client_email')
    if not client_email:
        flash('You must log in first.', 'danger')
        return redirect(url_for('clients.login'))

    client = Client.query.filter_by(emailaddress=client_email).first()
    client_name = client.name.capitalize() if client else "Client"

    return render_template('clients_dashboard.html', client_name=client_name)

@clients_bp.route('/book/<brand>', methods=['GET'])
def book_models(brand):
    models = db.session.query(Model).join(Car).filter(Car.brand.ilike(brand)).all()
    data = [
        {
            'modelid': m.modelid,
            'year': m.constructionyear,
            'color': m.color,
            'transmission': m.transmissiontype
        }
        for m in models
    ]
    return jsonify(models=data)

@clients_bp.route('/check_availability/<int:modelid>')
def check_availability(modelid):
    selected_date = request.args.get('date')

    # Query to check if car model already booked on that date
    rent = db.session.query(Rent).filter(
        Rent.modelid == modelid,
        Rent.date == selected_date
    ).first()

    if rent:
        return jsonify({'available': False})
    else:
        return jsonify({'available': True})



@clients_bp.route('/rentals', methods=['GET'])
def rentals():
    return "render_template('clients_rental.html')"

@clients_bp.route('/manage_creditcard', methods=['GET'])
def manage_creditcard():
    return "render_template('clients_manage_creditcard.html')"

@clients_bp.route('/manage_address', methods=['GET'])
def manage_address():
    return "render_template('clients_manage_address.html')"