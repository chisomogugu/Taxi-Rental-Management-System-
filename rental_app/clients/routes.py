from flask import Blueprint, render_template, request, flash, redirect, url_for
from rental_app import db
from rental_app.model import Client, Address, CreditCard, Rent, Model, Driver

clients_bp = Blueprint('clients', __name__)   # blueprint name: 'clients'

@clients_bp.route('/dashboard')
def dashboard():
    """Client dashboard home."""
    return render_template('clients/dashboard.html')

@clients_bp.route('/register', methods=('GET','POST'))
def register():
    """Client registration with one address & one credit card."""
    if request.method == 'POST':
        name   = request.form['name']
        email  = request.form['email']
        road   = request.form['road']
        number = int(request.form['number'])
        city   = request.form['city']
        card   = int(request.form['cardnumber'])
        # create client
        cl = Client(name=name, emailaddress=email)
        db.session.add(cl)
        # address record
        addr = Address(road=road, number=number, city=city)
        db.session.add(addr)
        # link client–address
        cl_addr = ClientAddress(emailaddress=email, road=road, number=number, city=city)
        db.session.add(cl_addr)
        # credit card
        cc = CreditCard(cardnumber=card, clientemail=email, road=road, number=number, city=city)
        db.session.add(cc)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('clients.dashboard'))
    return render_template('clients/register.html')

@clients_bp.route('/book_rent', methods=('GET','POST'))
def book_rent():
    """Book a rent for a given date and model."""
    if request.method == 'POST':
        email    = request.form['email']
        modelid  = int(request.form['modelid'])
        carid    = int(request.form['carid'])
        date_str = request.form['date']  # 'YYYY-MM-DD'
        # find an available driver who can drive that model
        # (omitted: you’d join Rent & DriverModel & Driver to find a free one)
        # Suppose you assign driver_name = 'SomeDriver'
        from datetime import datetime
        dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        rent = Rent(rentid=0, date=dt, clientemail=email,
                    drivername='SomeDriver', modelid=modelid, carid=carid)
        db.session.add(rent)
        db.session.commit()
        flash('Rent booked!', 'success')
        return redirect(url_for('clients.dashboard'))
    models = Model.query.all()
    return render_template('clients/book_rent.html', models=models)

@clients_bp.route('/my_rents')
def my_rents():
    """List all rents for a client (pass email as query param)."""
    email = request.args.get('email')
    rents = []
    if email:
        rents = Rent.query.filter_by(clientemail=email).all()
    return render_template('clients/list_rents.html', rents=rents)

@clients_bp.route('/review', methods=('GET','POST'))
def review_driver():
    """Submit a review for a driver after a completed rent."""
    if request.method == 'POST':
        email = request.form['email']
        driver = request.form['drivername']
        rating = int(request.form['rating'])
        msg    = request.form['message']
        rev = Review(reviewid=0, drivername=driver,
                     clientemail=email, rating=rating, message=msg)
        db.session.add(rev)
        db.session.commit()
        flash('Review submitted', 'success')
        return redirect(url_for('clients.dashboard'))
    # GET: show a simple form
    drivers = [d.name for d in Driver.query.all()]
    return render_template('clients/review_driver.html', drivers=drivers)
