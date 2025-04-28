from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class ClientRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    emailaddress = StringField('Email Address', validators=[DataRequired(), Email()])

    # Address
    road = StringField('Street Address', validators=[DataRequired(), Length(min=2, max=100)])
    number = IntegerField('Zip Code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])

    # Credit Card
    cardnumber = IntegerField('Credit Card Number', validators=[DataRequired(), NumberRange(min=1000000000000000, max=9999999999999999)])  # 16 digits
    card_road = StringField('Street Address', validators=[DataRequired(), Length(min=2, max=100)])
    card_number = IntegerField('Zip Code', validators=[DataRequired()])
    card_city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])

    submit = SubmitField('Register')

class ClientLoginForm(FlaskForm):
    emailaddress = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')
