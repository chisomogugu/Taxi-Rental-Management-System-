from rental_app import db
from rental_app.model import Car, Model
from sqlalchemy.exc import SQLAlchemyError

def add_car(carid, brand):
    try:
        car = Car(carid=carid, brand=brand)
        db.session.add(car)
        db.session.commit()
        return True, car
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def remove_car(carid):
    try:
        car = Car.query.get(carid)
        if not car:
            return False, 'Car not found'
        db.session.delete(car)
        db.session.commit()
        return True, None
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def add_model(modelid, carid, constructionyear, color, transmissiontype):
    try:
        model = Model(
          modelid=modelid,
          carid=carid,
          constructionyear=constructionyear,
          color=color,
          transmissiontype=transmissiontype
        )
        db.session.add(model)
        db.session.commit()
        return True, model
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def remove_model(modelid, carid):
    try:
        model = Model.query.get((modelid, carid))
        if not model:
            return False, 'Model not found'
        db.session.delete(model)
        db.session.commit()
        return True, None
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)
