from flask import render_template, redirect, url_for, flash, request, Blueprint
from rental_app import db
from rental_app.model import Driver, Address
from rental_app.drivers.forms import DriverLoginForm, DriverRegistrationForm

# Blueprint for the drivers module
drivers_bp = Blueprint('drivers', __name__, template_folder='templates')


# drivers login route
@drivers_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = DriverLoginForm()
    if form.validate_on_submit():
        try:
            # Check if the driver exists in the database
            driver = Driver.query.filter_by(name=form.name.data).first()
            if not driver:
                flash(f'Login failed. {form.name.data} not found.', 'danger')
                return redirect(url_for('drivers.login'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return
        flash('Login successful!', 'success')

        # Redirect to the driver's dashboard or another page
        return redirect(url_for('drivers.dashboard'))
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

    return render_template('drivers_register.html', form=form)



# drivers dashboard route
@drivers_bp.route('/dashboard')
def dashboard():
    # placeholder for the driver's dashboard
    return 'driver_dashboard.html'