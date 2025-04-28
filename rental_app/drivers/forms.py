from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class DriverRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    road = StringField('Street Address', validators=[DataRequired(), Length(min=2, max=100)])
    number = IntegerField('Zip Code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Register')

class DriverLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField('Login')