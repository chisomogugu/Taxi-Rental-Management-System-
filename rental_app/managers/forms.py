from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddCarForm(FlaskForm):
    license_plate = StringField("License Plate", validators=[DataRequired()])
    model_id = IntegerField("Model ID", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add Car")

class RemoveCarForm(FlaskForm):
    car_id = IntegerField("Car ID", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Remove Car")

class AddModelForm(FlaskForm):
    name = StringField("Model Name", validators=[DataRequired()])
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    submit = SubmitField("Add Model")

class RemoveModelForm(FlaskForm):
    model_id = IntegerField("Model ID", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Remove Model")
