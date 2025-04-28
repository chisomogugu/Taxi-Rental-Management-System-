from flask import render_template, redirect, url_for, flash, request, Blueprint
from rental_app import db
from rental_app.model import Manager
from rental_app.managers.forms import ManagerLoginForm, ManagerRegistrationForm


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
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return
        flash('Login successful!', 'success')
        # Redirect to the manager's dashboard
        return redirect(url_for('managers.dashboard'))
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

@managers_bp.route('/dashboard')
def dashboard():
    # This is a placeholder for the manager's dashboard
    return 'manager_dashboard.html'