# rental_app/drivers/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DriverLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Login')
