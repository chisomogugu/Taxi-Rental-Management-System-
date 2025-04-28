from flask import render_template, redirect, url_for, flash, request, Blueprint
from rental_app import db
from rental_app.model import Client, Address, CreditCard, ClientAddress
from rental_app.clients.forms import ClientRegistrationForm, ClientLoginForm

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

