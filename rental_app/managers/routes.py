from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from sqlalchemy import func
from sqlalchemy import desc, and_, distinct
from rental_app import db
from rental_app.model import Manager, Car, Driver, Model, Address, Client, Rent, ClientAddress, Review
from rental_app.managers.forms import ManagerLoginForm, ManagerRegistrationForm
from rental_app.managers.forms import AddCarForm, RemoveCarForm, AddModelForm, RemoveModelForm, AddDriverForm, RemoveDriverForm
from rental_app.managers.forms import TopKForm, CrossCityForm


managers_bp = Blueprint('managers', __name__, template_folder='templates')

@managers_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = ManagerLoginForm()
    if form.validate_on_submit():
        try:
            # Check if the manager exists in the database
            manager = Manager.query.filter_by(name=form.name.data, ssn=form.ssn.data).first()
            if not manager:
                flash(f'Login failed. {form.name.data} not found', 'danger')
                return redirect(url_for('managers.login')) 
            else:
                flash('Login successful!', 'success')
                session['managers_name'] = manager.name   #Save client email in session
                # Redirect to the manager's dashboard
                return redirect(url_for('managers.dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
        
    return render_template('manager_login.html', form=form)


# This route handles the registration of a new manager
@managers_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = ManagerRegistrationForm()

    if form.validate_on_submit():
        try:
            # Check if the manager already exists
            if Manager.query.filter_by(name=form.name.data).first():
                flash('Manager already exists.', 'danger')
                return redirect(url_for('managers.register'))
            
            # Create a new manager instance and add it to the database
            new_manager = Manager(name=form.name.data, ssn=form.ssn.data, email=form.email.data)
            db.session.add(new_manager)
            db.session.commit()
            flash('Registration successful!', 'success')
            # Redirect to the login page
            return redirect(url_for('managers.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    return render_template('manager_register.html', form=form)

@managers_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # instantiate the four forms
    add_car_form       = AddCarForm()
    remove_car_form    = RemoveCarForm()
    add_model_form     = AddModelForm()
    remove_model_form  = RemoveModelForm()
    add_driver_form   = AddDriverForm()    
    remove_driver_form= RemoveDriverForm()

    return render_template(
        'manager_dashboard.html',
        add_car_form=add_car_form,
        remove_car_form=remove_car_form,
        add_model_form=add_model_form,
        remove_model_form=remove_model_form,
        add_driver_form=add_driver_form,  
        remove_driver_form=remove_driver_form
)


######################## ADD/REMOVE CAR ############################

@managers_bp.route('/add_car', methods=['POST'])
def add_car():
    form = AddCarForm()
    if form.validate_on_submit():

        # Check if the car already exists
        if Car.query.filter_by(carid=form.carid.data).first():
            flash("CarID already exist", 'danger')
            return redirect(url_for('managers.dashboard'))
        
        #Create new car type
        new_car = Car(
            carid=form.carid.data,
            brand=form.brand.data
        )
        db.session.add(new_car)
        try:
            db.session.commit()
            flash(f"{new_car.brand} with ID #{new_car.carid} successfully added.", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while adding car: {str(e)}')
    return redirect(url_for('managers.dashboard'))


@managers_bp.route('/remove_car', methods=['POST'])
def remove_car():
    form = RemoveCarForm()
    if form.validate_on_submit():
        car = Car.query.get(form.car_id.data)
        try:
            if car:
                # Remove all models associated with this car
                for model in car.models:
                    # Remove all rentals associated with this model
                    for rent in model.rents:
                        db.session.delete(rent)
                    db.session.delete(model)

                db.session.delete(car)
                db.session.commit()
                flash(f"{car.brand} with ID #{car.carid} successfully removed.", 'success')
            else:
                flash('Car not found.', 'warning')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while removing car: {str(e)}', 'danger')

    return redirect(url_for('managers.dashboard'))


######################## ADD/REMOVE MODEL ############################
@managers_bp.route('/add_model', methods=['POST'])
def add_model():
    form = AddModelForm()
    if form.validate_on_submit():
        # Checks if the car exists
        car = Car.query.get(form.carid.data)
        if not car:
            flash('Invalid Car ID.', 'danger')
            return redirect(url_for('managers.dashboard'))
        
        # Check if the model already exists
        if Model.query.filter_by(modelid=form.modelid.data, carid=form.carid.data).first():
            flash('Model already exists.', 'danger')
            return redirect(url_for('managers.dashboard'))
        
        # Create a new model instance
        new_model = Model(
            modelid=form.modelid.data,
            carid=form.carid.data,
            constructionyear=form.constructionyear.data,
            color=form.color.data,
            transmissiontype=form.transmissiontype.data
        )
        db.session.add(new_model)
        try:
            db.session.commit()
            flash(f'Model {new_model.modelid} added to CarID #{new_model.carid}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding model: {e}', 'danger')
    else:
        flash('Failed to add model. Please check your input.', 'danger')
    return redirect(url_for('managers.dashboard'))

@managers_bp.route('/remove_model', methods=['POST'])
def remove_model():
    form = RemoveModelForm()
    if form.validate_on_submit():
        model = Model.query.filter_by(modelid=form.model_id.data, carid=form.car_id.data).first()
        if not model:
            flash('Model not found.', 'danger')
        else:
            # delete all Rent rows that point at this model
            for rent in list(model.rents):
                db.session.delete(rent)

            # delete all DriverModel rows that point at this model
            for dm in list(model.driver_models):
                db.session.delete(dm)
            # now safe to delete the model
            db.session.delete(model)
            db.session.commit()
            flash(f'Model #{form.model_id.data} removed', 'success')
    else:
        flash('Invalid Model ID.', 'danger')
    return redirect(url_for('managers.dashboard'))

######################## ADD/REMOVE DRIVER ############################
@managers_bp.route('/add_driver', methods=['POST'])
def add_driver():
    form = AddDriverForm()
    if form.validate_on_submit():
        name = form.driver_name.data

        # Check if driver already exists
        if Driver.query.get(name):
            flash(f"Driver '{name}' already exists.", 'warning')
            return redirect(url_for('managers.dashboard'))

        # Check if address exists
        addr = Address.query.filter_by(
            road=form.road.data,
            number=form.number.data,
            city=form.city.data
        ).first()

        # If address doesn't exist, create a new one
        if not addr:
            try:
                addr = Address(
                    road=form.road.data,
                    number=form.number.data,
                    city=form.city.data
                )
                db.session.add(addr)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding address: {e}', 'danger')
                return redirect(url_for('managers.dashboard'))

        # Add the new driver
        try:
            new_driver = Driver(
                name=name,
                road=addr.road,
                number=addr.number,
                city=addr.city
            )
            db.session.add(new_driver)
            db.session.commit()
            flash(f"{name} has been added as a driver", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding driver: {e}', 'danger')

    else:
        flash("Invalid form submission.", 'danger')

    return redirect(url_for('managers.dashboard'))


# Remove a driver route
@managers_bp.route('/remove_driver', methods=['POST'])
def remove_driver():
    form = RemoveDriverForm()
    if form.validate_on_submit():
        name = form.driver_name.data

        # Check if driver exists
        driver = Driver.query.get(name)
        if not driver:
            flash(f"Driver '{name}' not found.", 'danger')
        else:
            try:
                # Remove linked entries
                for rent in driver.rents:
                    db.session.delete(rent)
                for rev in driver.reviews:
                    db.session.delete(rev)
                for dm in driver.driver_models:
                    db.session.delete(dm)

                # Remove the driver
                db.session.delete(driver)
                db.session.commit()
                flash(f"{name} has been removed as a driver.", 'success')
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while removing the driver: {e}", 'danger')
    else:
        flash('Invalid driver name.', 'danger')

    return redirect(url_for('managers.dashboard'))



####################### NAVBAR ####################################

#Finds the top k clients with the most rentals
@managers_bp.route('/top_k_clients', methods=['GET','POST'])
def top_k_clients():
    form = TopKForm()
    clients = []
    if form.validate_on_submit():
        k = form.k.data
        # count rents per client
        rows = (db.session.query(
                    Client.name,
                    Client.emailaddress,func.count(Rent.rentid).label('rentals')
                    )
              .join(Rent, Rent.clientemail == Client.emailaddress)
              .group_by(Client.name, Client.emailaddress)
              .order_by(desc('rentals'))
              .limit(k)
              .all()
        )
        clients = [{'name': n, 'email': e, 'rentals': r} for n,e,r in rows]

    return render_template(
        'manager_top_k_clients.html',
        form=form,
        clients=clients
    )

# Finds clients who rented cars in two different cities
@managers_bp.route('/cross_city_clients', methods=['GET','POST'])
def cross_city_clients():
    form = CrossCityForm()
    results = []
    if form.validate_on_submit():
        c1 = form.city1.data
        c2 = form.city2.data

        # build the query
        rows = (
            db.session
              .query(
                Client.name.label('name'),
                Client.emailaddress.label('email')
              )
              # “Home” address in C1:
              .join(ClientAddress, Client.emailaddress == ClientAddress.emailaddress)
              .filter(ClientAddress.city == c1)
              # at least one rent whose driver lives in C2:
              .join(Rent, Rent.clientemail == Client.emailaddress)
              .join(Driver,   Rent.drivername == Driver.name)
              .filter(Driver.city == c2)
              .distinct()   # don't list the same client twice
              .all()
        )

        results = [{'name': n, 'email': e} for n, e in rows]

        if not results:
            flash(f'No cross-city clients found for C₁={c1}, C₂={c2}', 'warning')

    return render_template(
        'manager_cross_city_clients.html',
        form=form,
        clients=results
    )



@managers_bp.route('/model_usage_stats', methods=['GET','POST'])
def model_usage_stats():
    """
    For every Model (modelid + carid): show brand, modelid, color,
    and total number of rents it has been used.
    """
    rows = (
        db.session
          .query(
            Model.modelid.label('modelid'),
            Car.brand.label('brand'),
            Model.color.label('color'),
            func.count(Rent.rentid).label('rent_count')
          )
          .join(Car, Model.carid == Car.carid)
          # include models even if they have zero rentals
          .outerjoin(
             Rent,
             and_(
               Rent.modelid == Model.modelid,
               Rent.carid   == Model.carid
             )
          )
          .group_by(Model.modelid, Car.brand, Model.color)
          .order_by(Car.brand, Model.modelid)
          .all()
    )

    stats = []
    for modelid, brand, color, rent_count in rows:
        stats.append({
            'label':f"{brand} (Model #{modelid}, {color})",
            'rent_count': rent_count
        })

    return render_template('manager_model_usage.html', stats=stats)

@managers_bp.route('/driver_performancel', methods=['GET','POST'])
def driver_performance():
    """
    For every Driver X: show X.name, total number of rents X did,
    and X's average review rating.
    """
    rows = (
        db.session
          .query(
            Driver.name.label('name'),
            func.count(Rent.rentid).label('rent_count'),
            func.avg(Review.rating).label('avg_rating')
          )
          # include drivers even if they have zero rents / zero reviews
          .outerjoin(Rent,   Rent.drivername   == Driver.name)
          .outerjoin(Review, Review.drivername == Driver.name)
          .group_by(Driver.name)
          .order_by(desc('rent_count'))
          .all()
    )

    perf = []
    for name, rent_count, avg_rating in rows:
        perf.append({
            'name':       name,
            'rent_count': rent_count,
            'avg_rating': round(avg_rating or 0, 2)
        })

    return render_template('manager_driver_performance.html', perf=perf)
