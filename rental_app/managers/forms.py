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

class AddCarForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    carid = IntegerField('Car ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Car')

class RemoveCarForm(FlaskForm):
    car_id = IntegerField('Car ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Remove Car')

class AddModelForm(FlaskForm):
    modelid = IntegerField('Model ID',validators=[DataRequired(), NumberRange(min=1)])
    carid = IntegerField('Car ID', validators=[DataRequired(), NumberRange(min=1)])
    constructionyear = IntegerField('Construction Year', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    transmissiontype = StringField('Transmission Type', validators=[DataRequired()])
    submit = SubmitField('Add Model')

class RemoveModelForm(FlaskForm):
    model_id = IntegerField('Model ID', validators=[DataRequired(), NumberRange(min=1)])
    car_id = IntegerField('Car ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Remove Model')

class TopKForm(FlaskForm):
    k = IntegerField('Number of clients', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Show Top Clients')

class CrossCityForm(FlaskForm):
    city1 = StringField('Client City (C₁)', validators=[DataRequired()])
    city2 = StringField('Driver City (C₂)', validators=[DataRequired()])
    submit = SubmitField('Show Clients')

class AddDriverForm(FlaskForm):
    driver_name = StringField('Driver Name', validators=[DataRequired(), Length(max=100)])
    road = StringField('Road',validators=[DataRequired(), Length(max=100)])
    number = IntegerField('Zip Code', validators=[DataRequired(), NumberRange(min=1)])
    city = StringField('City', validators=[DataRequired(), Length(max=50)] )
    submit = SubmitField('Add Driver')

class RemoveDriverForm(FlaskForm):
    driver_name = StringField('Driver Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Remove Driver')