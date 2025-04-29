from flask import render_template, redirect, url_for, flash, jsonify,request, session, Blueprint
from rental_app import db
from rental_app.model import Driver, Address, DriverModel, Rent, Car,Model
from rental_app.drivers.forms import DriverLoginForm, DriverRegistrationForm, DriverUpdateAddressForm

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
        'modelid': m.modelid,
        'year': m.constructionyear,
        'color': m.color,
        'transmission': m.transmissiontype
    } for m in models])

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
@drivers_bp.route('/show_drivers_models', methods=['GET', 'POST'])
def view_drivers_models():
    drivers = Driver.query.all()
    return "render_template('drivers_model.html', drivers=drivers)"

# drivers rentals route
@drivers_bp.route('/rentals', methods=['GET', 'POST'])
def rentals():
    return "render_template('drivers_rentals.html')"

# drivers declare_models route
@drivers_bp.route('/declare_models', methods=['GET', 'POST'])
def declare_models():
    return "render_template('drivers_declare_models.html')"