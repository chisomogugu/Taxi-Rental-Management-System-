from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import func, desc
from rental_app import db
from rental_app.model import Client, Rent, Driver, Review, Model, Car, Address, ClientAddress, CreditCard, DriverModel

managers_bp = Blueprint('managers', __name__, template_folder='../templates/managers')

# ──────────────────────────────────────────────────────────────────────────────
# 1) Dashboard
@managers_bp.route('/dashboard')
def dashboard():
    return render_template('managers/dashboard.html')


# ──────────────────────────────────────────────────────────────────────────────
# 2) Top-K Clients
@managers_bp.route('/dashboard/top_k_clients', methods=('GET','POST'))
def top_k_clients():
    results = []
    k = None
    if request.method == 'POST':
        try:
            k = int(request.form['k'])
            # count rents per client, order desc, limit k
            results = (
                db.session.query(
                    Client.name,
                    Client.emailaddress,
                    func.count(Rent.rentid).label('num_rents')
                )
                .join(Rent, Rent.clientemail == Client.emailaddress)
                .group_by(Client.emailaddress, Client.name)
                .order_by(desc('num_rents'))
                .limit(k)
                .all()
            )
        except ValueError:
            flash('Please enter a valid integer for k.', 'warning')
    return render_template('managers/top_k_clients.html', results=results, k=k)


# ──────────────────────────────────────────────────────────────────────────────
# 3) Model Usage Stats
@managers_bp.route('/dashboard/model_usage_stats')
def model_usage_stats():
    stats = (
        db.session.query(
            Model.modelid,
            Model.carid,
            func.count(Rent.rentid).label('usage_count')
        )
        .outerjoin(Rent, (Rent.modelid == Model.modelid) & (Rent.carid == Model.carid))
        .group_by(Model.modelid, Model.carid)
        .all()
    )
    return render_template('managers/model_usage_stats.html', stats=stats)


# ──────────────────────────────────────────────────────────────────────────────
# 4) Driver Performance
@managers_bp.route('/dashboard/driver_performance')
def driver_performance():
    perf = (
        db.session.query(
            Driver.name,
            func.count(Rent.rentid).label('num_rents'),
            func.coalesce(func.avg(Review.rating), 0).label('avg_rating')
        )
        .outerjoin(Rent, Rent.drivername == Driver.name)
        .outerjoin(Review, Review.drivername == Driver.name)
        .group_by(Driver.name)
        .all()
    )
    return render_template('managers/driver_performance.html', perf=perf)


# ──────────────────────────────────────────────────────────────────────────────
# 5) Cross-City Clients
@managers_bp.route('/dashboard/cross_city_clients', methods=('GET','POST'))
def cross_city_clients():
    clients = []
    c1 = c2 = None
    if request.method == 'POST':
        c1 = request.form['city1']
        c2 = request.form['city2']
        # clients with an address in c1
        # AND who booked a rent whose driver has an address in c2
        sub = (
            db.session.query(Rent.clientemail)
            .join(Driver, Rent.drivername == Driver.name)
            .filter(Driver.city == c2)
            .subquery()
        )
        clients = (
            db.session.query(Client.name, Client.emailaddress)
            .join(ClientAddress, ClientAddress.emailaddress == Client.emailaddress)
            .filter(ClientAddress.city == c1)
            .filter(Client.emailaddress.in_(sub))
            .all()
        )
    return render_template(
        'managers/cross_city_clients.html',
        clients=clients,
        c1=c1,
        c2=c2
    )


# ──────────────────────────────────────────────────────────────────────────────
# 6) Add Car
@managers_bp.route('/dashboard/add_car', methods=('GET','POST'))
def add_car():
    if request.method == 'POST':
        try:
            cid = int(request.form['carid'])
            brand = request.form['brand']
            db.session.add(Car(carid=cid, brand=brand))
            db.session.commit()
            flash('Car added successfully!', 'success')
            return redirect(url_for('managers.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding car: {e}', 'danger')
    return render_template('managers/add_car.html')


# ──────────────────────────────────────────────────────────────────────────────
# 7) Remove Car
@managers_bp.route('/dashboard/remove_car', methods=('GET','POST'))
def remove_car():
    if request.method == 'POST':
        try:
            cid = int(request.form['carid'])
            car = Car.query.get(cid)
            db.session.delete(car)
            db.session.commit()
            flash('Car removed.', 'success')
            return redirect(url_for('managers.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error removing car: {e}', 'danger')
    return render_template('managers/remove_car.html')


# ──────────────────────────────────────────────────────────────────────────────
# 8) Add Model
@managers_bp.route('/dashboard/add_model', methods=('GET','POST'))
def add_model():
    cars = Car.query.all()
    if request.method == 'POST':
        try:
            mid = int(request.form['modelid'])
            cid = int(request.form['carid'])
            year = int(request.form['year'])
            color = request.form['color']
            trans = request.form['transmission']
            db.session.add(
                Model(
                    modelid=mid,
                    carid=cid,
                    constructionyear=year,
                    color=color,
                    transmissiontype=trans
                )
            )
            db.session.commit()
            flash('Model added successfully!', 'success')
            return redirect(url_for('managers.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding model: {e}', 'danger')
    return render_template('managers/add_model.html', cars=cars)


# ──────────────────────────────────────────────────────────────────────────────
# 9) Remove Model
@managers_bp.route('/dashboard/remove_model', methods=('GET','POST'))
def remove_model():
    if request.method == 'POST':
        try:
            mid = int(request.form['modelid'])
            cid = int(request.form['carid'])
            m = Model.query.get((mid, cid))
            db.session.delete(m)
            db.session.commit()
            flash('Model removed.', 'success')
            return redirect(url_for('managers.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error removing model: {e}', 'danger')
    return render_template('managers/remove_model.html')
