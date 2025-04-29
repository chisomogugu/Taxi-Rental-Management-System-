from flask import render_template, redirect, url_for, flash, jsonify,request, session, Blueprint
from rental_app import db
from rental_app.model import Driver, Address, DriverModel, Rent, Car,Model, Client
from rental_app.drivers.forms import DriverLoginForm, DriverRegistrationForm, DriverUpdateAddressForm
from datetime import datetime

# Blueprint for the drivers module
drivers_bp = Blueprint('drivers', __name__, template_folder='templates')


# drivers login route
@drivers_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = DriverLoginForm()
    if form.validate_on_submit():
        # Check if the driver exists
        driver = Driver.query.filter_by(name=form.name.data).first()

        if driver:
            flash('Login successful!', 'success')
            session['driver_name'] = driver.name  # Save login session
            return redirect(url_for('drivers.dashboard'))
        else:
            flash('Login failed. Driver not found.', 'danger')
            return redirect(url_for('drivers.register'))

    return render_template('drivers_login.html', form=form)

# drivers register route
@drivers_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = DriverRegistrationForm()

    if form.validate_on_submit():
        try:
            # Check if the driver already exists
            if Driver.query.filter_by(name=form.name.data).first():
                flash('Driver already exists.', 'danger')
                return redirect(url_for('drivers.register'))

            # Check if the address already exists
            address = Address.query.filter_by(
                road=form.road.data,
                number=form.number.data,
                city=form.city.data
            ).first()

            # Create a new address if it doesn't exist
            if not address:
                new_address = Address(
                    road=form.road.data,
                    number=form.number.data,
                    city=form.city.data
                )
                db.session.add(new_address)
                db.session.commit()

            #create the new driver
            new_driver = Driver(
                name=form.name.data,
                road=form.road.data,
                number=form.number.data,
                city=form.city.data
            )
            db.session.add(new_driver)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('drivers.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('drivers.register'))

    return render_template('drivers_register.html', form=form)

# drivers dashboard route
@drivers_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'driver_name' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('drivers.login'))

    driver = Driver.query.filter_by(name=session['driver_name']).first()
    cars = Car.query.all()  # Get all car brands from the database
    return render_template('drivers_dashboard.html', driver=driver, cars=cars)

@drivers_bp.route('/carinventory/<brand>', methods=['GET'])
def get_models(brand):
    # Join Model with Car to get models that belong to this brand
    models = db.session.query(Model).join(Car, Model.carid == Car.carid).filter(Car.brand == brand).all()
    
    return jsonify(models=[{
        'carid': m.carid,
        'modelid': m.modelid,
        'constructionyear': m.constructionyear,
        'color': m.color,
        'transmissiontype': m.transmissiontype
    } for m in models])

# update driver model route
@drivers_bp.route('/update_drivers_model', methods=['POST'])
def update_drivers_model():
    if 'driver_name' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('drivers.login'))

    driver_name = session['driver_name']
    modelid = request.form.get('modelid')
    carid = request.form.get('carid')

    if not modelid or not carid:
        flash('Invalid model or car selection.', 'danger')
        return redirect(url_for('drivers.dashboard'))

    # Check if already added
    existing = DriverModel.query.filter_by(
        drivername=driver_name,
        modelid=modelid,
        carid=carid
    ).first()

    if existing:
        flash('Model already added to your list.', 'info')
    else:
        try:
            new_driver_model = DriverModel(
                drivername=driver_name,
                modelid=modelid,
                carid=carid
            )
            db.session.add(new_driver_model)
            db.session.commit()
            flash('Model added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding model: {str(e)}', 'danger')

    return redirect(url_for('drivers.dashboard'))

# drivers update address route
@drivers_bp.route('/update_address', methods=['GET', 'POST'])
def update_address():
    if 'driver_name' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('drivers.login'))

    driver = Driver.query.filter_by(name=session['driver_name']).first()
    if not driver:
        flash('Driver not found.', 'danger')
        return redirect(url_for('drivers.login'))

    form = DriverUpdateAddressForm()

    if form.validate_on_submit():
        try:
            # Check if the new address exists
            existing_address = Address.query.filter_by(
                road=form.road.data,
                number=form.number.data,
                city=form.city.data
            ).first()

            if not existing_address:
                new_address = Address(
                    road=form.road.data,
                    number=form.number.data,
                    city=form.city.data
                )
                db.session.add(new_address)
                db.session.commit()

            # Update driver's own address
            driver.road = form.road.data
            driver.number = form.number.data
            driver.city = form.city.data
            db.session.commit()

            flash('Address updated successfully!', 'success')
            return redirect(url_for('drivers.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating address: {str(e)}', 'danger')
            return redirect(url_for('drivers.update_address'))

    return render_template('update_address.html', form=form)

# show all drivers models route
@drivers_bp.route('/view_drivers_models', methods=['GET'])
def view_drivers_models():
    # Check if the driver is logged in
    if 'driver_name' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('drivers.login'))

    # Get the driver name from the session
    driver_name = session['driver_name']
    
    # Join DriverModel to Model and Car tables to get all model info
    driver_models = db.session.query(DriverModel, Model, Car).\
        join(Model, DriverModel.modelid == Model.modelid).\
        join(Car, DriverModel.carid == Car.carid).\
        filter(DriverModel.drivername == driver_name).all()

    return render_template('drivers_models.html', driver_models=driver_models)

# Remove mode from drivers list route
@drivers_bp.route('/remove_model', methods=['POST'])
def remove_model():
    if 'driver_name' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('drivers.login'))

    # Check if the driver is logged in
    modelid = request.form.get('modelid')
    carid = request.form.get('carid')
    drivername = session['driver_name']

    if not modelid or not carid:
        flash('Invalid request.', 'danger')
        return redirect(url_for('drivers.view_drivers_models'))

    # Check if the model exists in the driver's list
    entry = DriverModel.query.filter_by(
        drivername=drivername,
        modelid=modelid,
        carid=carid
    ).first()
    
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash('Model removed successfully!', 'success')
    else:
        flash('Model not found in your list.', 'warning')

    return redirect(url_for('drivers.view_drivers_models'))

# drivers rentals route
@drivers_bp.route('/rentals', methods=['GET', 'POST'])
def rentals():
    if 'driver_name' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('drivers.login'))

    driver_name = session['driver_name']
    today = datetime.today().date()

    # Query all bookings for this driver
    rentals = Rent.query.filter_by(drivername=driver_name).all()

    today_rentals = {}
    upcoming_rentals = {}
    past_rentals = {}

    for rent in rentals:
        rent_date = rent.date
        client_name = Client.query.filter_by(emailaddress=rent.clientemail).first()
        if rent_date == today:
            today_rentals[client_name] = rent
        elif rent_date > today:
            upcoming_rentals[client_name] = rent
        else:
            past_rentals[client_name] = rent

    return render_template('drivers_rentals.html',
                           today_rentals=today_rentals,
                           upcoming_rentals=upcoming_rentals,
                           past_rentals=past_rentals)
