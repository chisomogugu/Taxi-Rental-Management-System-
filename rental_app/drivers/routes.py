from flask import Blueprint, render_template, request, flash, redirect, url_for
from rental_app import db
from rental_app.model import Driver, Address, DriverModel, Model

drivers_bp = Blueprint('drivers', __name__)    # blueprint name: 'drivers'

@drivers_bp.route('/dashboard')
def dashboard():
    """Driver dashboard home."""
    return render_template('drivers/dashboard.html')

@drivers_bp.route('/login', methods=('GET','POST'))
def login():
    """Driver login form."""
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        # ... login logic here ...
        flash(f'Logged in as {name}', 'success')
        return redirect(url_for('drivers.dashboard'))
    return render_template('drivers/login.html')

@drivers_bp.route('/update_address', methods=('GET','POST'))
def update_address():
    """Form for driver to change their address."""
    if request.method == 'POST':
        name     = request.form['name']
        new_road = request.form['road']
        new_num  = request.form['number']
        new_city = request.form['city']
        # look up and update
        drv = Driver.query.filter_by(name=name).first()
        if not drv:
            flash('Driver not found', 'danger')
        else:
            # ensure address record exists
            addr = Address.query.get((new_road, int(new_num), new_city))
            if not addr:
                addr = Address(road=new_road, number=int(new_num), city=new_city)
                db.session.add(addr)
            drv.road, drv.number, drv.city = new_road, int(new_num), new_city
            db.session.commit()
            flash('Address updated', 'success')
            return redirect(url_for('drivers.dashboard'))
    return render_template('drivers/update_address.html')

@drivers_bp.route('/select_models', methods=('GET','POST'))
def select_models():
    """Form for driver to declare which models they can drive."""
    if request.method == 'POST':
        name   = request.form['name']
        modelid = int(request.form['modelid'])
        carid   = int(request.form['carid'])
        drv = Driver.query.filter_by(name=name).first()
        mdl = Model.query.get((modelid, carid))
        if not drv or not mdl:
            flash('Driver or Model not found', 'danger')
        else:
            link = DriverModel(drivername=drv.name, modelid=modelid, carid=carid)
            db.session.add(link)
            db.session.commit()
            flash('Model added to driver profile', 'success')
            return redirect(url_for('drivers.dashboard'))
    # GET: just render form
    cars = Model.query.all()
    return render_template('drivers/select_models.html', models=cars)
