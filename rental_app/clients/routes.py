from flask import render_template, redirect, jsonify, url_for, flash, session, request, Blueprint
from rental_app import db
import random
from rental_app.model import Client, Address, CreditCard, ClientAddress, Car, Model, Rent, Review, DriverModel
from rental_app.clients.forms import ClientRegistrationForm, ClientLoginForm

#Contains view functions that handle HTTP requests and define URL endpoints
clients_bp = Blueprint('clients', __name__, template_folder='templates')

@clients_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = ClientLoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(emailaddress=form.emailaddress.data).first()
        if client:
            session['client_email'] = client.emailaddress   #Save client email in session
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

    # Get all car brands from the database
    cars = Car.query.all()
    return render_template('clients_dashboard.html', client_name=client_name, cars=cars)

@clients_bp.route('/book/<brand>', methods=['GET'])
def book_models(brand):
    models = db.session.query(Model, Car).join(Car).filter(Car.brand.ilike(brand)).all()
    data = [
        {
            'modelid': m.Model.modelid,
            'year': m.Model.constructionyear,
            'color': m.Model.color,
            'transmission': m.Model.transmissiontype,
            'brand': m.Car.brand,
            'name': f"{m.Car.brand} {m.Model.color} {m.Model.transmissiontype} {m.Model.constructionyear}"  # 💡 Name
        }
        for m in models
    ]
    return jsonify(models=data)

@clients_bp.route('/check_availability/<int:modelid>')
def check_availability(modelid):
    selected_date = request.args.get('date')

    # Check if the model is already rented
    rented = db.session.query(Rent).filter_by(modelid=modelid, date=selected_date).first()
    if rented:
        return jsonify({'available': False})

    # Get all drivers that can drive this model
    from rental_app.model import DriverModel  # import if not already
    driver_models = DriverModel.query.filter_by(modelid=modelid).all()
    driver_names = [dm.drivername for dm in driver_models]

    if not driver_names:
        return jsonify({'available': False})

    # Check if any driver is available (i.e., not assigned on that date)
    busy_drivers = db.session.query(Rent.drivername).filter(Rent.date == selected_date).all()
    busy_names = {d.drivername for d in busy_drivers}

    available_driver = next((name for name in driver_names if name not in busy_names), None)

    return jsonify({'available': bool(available_driver)})


@clients_bp.route('/profile_data')
def profile_data():
    client_email = session.get('client_email')
    if not client_email:
        return jsonify({'error': 'Unauthorized'}), 401


@clients_bp.route('/my_rentals', methods=['GET'])
def my_rentals():
    client_email = session.get('client_email')
    if not client_email:
        return jsonify({'error': 'Unauthorized'}), 401

    rentals = db.session.query(Rent, Model).join(Model, Rent.modelid == Model.modelid)\
        .filter(Rent.clientemail == client_email).all()

    data = []
    for rent, model in rentals:
        review_exists = db.session.query(Review).filter_by(
            drivername=rent.drivername,
            clientemail=client_email
        ).first() is not None

        data.append({
            'rentid': rent.rentid,
            'date': rent.date.strftime('%Y-%m-%d'),
            'drivername': rent.drivername,
            'constructionyear': model.constructionyear,
            'color': model.color,
            'transmissiontype': model.transmissiontype,
            'canReview': not review_exists  # 👈 new flag
        })

    return jsonify(data)

@clients_bp.route('/rental_history')
def rental_history():
    return render_template('clients_rental.html')

@clients_bp.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        data = request.get_json()
        client_email = session.get('client_email')
        if not client_email:
            return jsonify({'error': 'Unauthorized'}), 401

        drivername = data['drivername']
        rating = int(data['rating'])
        message = data['message'][:255]  # Limit message length

        # Check if this driver was already reviewed by this client
        existing = Review.query.filter_by(
            drivername=drivername,
            clientemail=client_email
        ).first()

        if existing:
            return jsonify({'error': 'You already reviewed this driver.'}), 400

        # Generate review ID
        total_reviews = Review.query.count()

        review = Review(
            reviewid=total_reviews + 1,
            drivername=drivername,
            clientemail=client_email,
            message=message,
            rating=rating
        )

        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review submitted successfully!'})

    except Exception as e:
        db.session.rollback()
        print("Error submitting review:", e)
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    try:
        data = request.get_json()
        modelid = int(data['modelid'])
        date = data['date']
        client_email = session.get('client_email')

        if not client_email:
            return jsonify({'error': 'Unauthorized'}), 401

        #Get all drivers for this model
        drivers = DriverModel.query.filter_by(modelid=modelid).all()
        all_driver_names = [d.drivername for d in drivers]

        #Remove busy drivers
        busy_drivers = {r.drivername for r in Rent.query.filter_by(date=date).all()}
        available_drivers = [d for d in all_driver_names if d not in busy_drivers]

        if not available_drivers:
            return jsonify({'error': 'No available drivers for this model on that date.'}), 400

        # Randomly choose one driver
        assigned_driver = random.choice(available_drivers)

        # Get carid for this model
        car = Model.query.filter_by(modelid=modelid).first()
        if not car:
            return jsonify({'error': 'Model not found'}), 400

        # Generate unique rentid
        existing_ids = {r[0] for r in db.session.query(Rent.rentid).all()}
        rentid = random.randint(1000, 9999)
        while rentid in existing_ids:
            rentid = random.randint(1000, 9999)

        # Step 6: Insert new rent record
        new_rent = Rent(
            rentid=rentid,
            date=date,
            drivername=assigned_driver,
            clientemail=client_email,
            modelid=modelid,
            carid=car.carid
        )
        db.session.add(new_rent)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        print("Booking error:", str(e))
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/manage_creditcard', methods=['GET', 'POST'])
def manage_creditcard():
    if 'client_email' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('clients.login'))

    email = session['client_email']

    # All cards for this client
    cards = CreditCard.query.filter_by(clientemail=email).all()

    try:
        if request.method == 'POST':
            action = request.form.get('action')
            old_card = request.form.get('original_card')
            cardnumber = request.form.get('cardnumber')
            road = request.form.get('road')
            number = request.form.get('number')
            city = request.form.get('city')

            if action == 'update':
                existing_card = CreditCard.query.filter_by(cardnumber=old_card).first()
                if existing_card:
                    # Step 1: Ensure new address exists in Address table
                    address = Address.query.filter_by(road=road, number=number, city=city).first()
                    if not address:
                        address = Address(road=road, number=number, city=city)
                        db.session.add(address)
                        db.session.commit()

                    # Step 2: Update the fields directly
                    existing_card.cardnumber = cardnumber
                    existing_card.road = road
                    existing_card.number = number
                    existing_card.city = city

                    db.session.commit()
                    flash('Card updated successfully.', 'success')
                else:
                    flash('Card not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')

        return redirect(url_for('clients.manage_creditcard'))

    return render_template('client_manage_creditcard.html', cards=cards)

@clients_bp.route('/manage_address', methods=['GET', 'POST'])
def manage_address():
    if 'client_email' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('clients.login'))

    email = session['client_email']

    # Get all the client's addresses
    addresses = ClientAddress.query.filter_by(emailaddress=email).all()

    if request.method == 'POST':
        action = request.form.get('action')
        road = request.form.get('road')
        number = request.form.get('number')
        city = request.form.get('city')

        if action == 'add':
            # Check if Address exists
            address = Address.query.filter_by(
                road=road, number=number, city=city
            ).first()

            if not address:
                address = Address(road=road, number=number, city=city)
                db.session.add(address)
                db.session.commit()
            
            # Check for duplicates
            exists = ClientAddress.query.filter_by(
                emailaddress=email,
                road=road,
                number=number,
                city=city
            ).first()
            if exists:
                flash('Address already exists.', 'warning')
            else:
                new_address = ClientAddress(
                    emailaddress=email,
                    road=road,
                    number=number,
                    city=city
                )
                db.session.add(new_address)
                db.session.commit()
                flash('Address added successfully!', 'success')

        elif action == 'delete':
            addr = ClientAddress.query.filter_by(
                emailaddress=email,
                road=road,
                number=number,
                city=city
            ).first()

            if addr:
                total = ClientAddress.query.filter_by(emailaddress=email).count()
                if total > 1:
                    db.session.delete(addr)
                    db.session.commit()
                    flash('Address deleted.', 'success')
                else:
                    flash('You must have at least one address.', 'danger')
            else:
                flash('Address not found.', 'warning')

        elif action == 'update':
            original = request.form.get('original')
            orig_road, orig_number, orig_city = original.split('|')

            # Step 1: Delete old ClientAddress link
            old_link = ClientAddress.query.filter_by(
                emailaddress=email,
                road=orig_road,
                number=orig_number,
                city=orig_city
            ).first()

            if old_link:
                db.session.delete(old_link)

                # Step 2: Check if new address exists in Address table
                existing_address = Address.query.filter_by(
                    road=road,
                    number=number,
                    city=city
                ).first()

                if not existing_address:
                    new_address = Address(road=road, number=number, city=city)
                    db.session.add(new_address)

                # Step 3: Add new link to ClientAddress
                new_link = ClientAddress(
                    emailaddress=email,
                    road=road,
                    number=number,
                    city=city
                )
                db.session.add(new_link)

                db.session.commit()
                flash('Address updated successfully!', 'success')
            else:
                flash('Original address not found.', 'danger')

        return redirect(url_for('clients.manage_address'))

    return render_template('client_manage_address.html', addresses=addresses)

    