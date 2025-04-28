from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class ManagerRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    ssn = IntegerField('SSN', validators=[DataRequired(), NumberRange(min=100000000, max=999999999)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class ManagerLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField('Login')
