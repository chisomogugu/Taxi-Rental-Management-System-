#------
# Register Client, Manager, and Driver

from sqlalchemy.exc import SQLAlchemyError
from rental_app import db
from rental_app.model import Manager, Address, Driver, Car, Model, DriverModel
from rental_app.model import Review, Rent, ClientAddress, CreditCard, Client
from sqlalchemy import func, and_, not_, exists
from datetime import datetime

def registers_manager(name, ssn, email):
    """
    Registers a new manager to the database.
    """
    try:
        new_manager = Manager(name=name, ssn=ssn, email=email)
        db.session.add(new_manager)
        db.session.commit()
        return True, new_manager
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def login_manager(name, ssn, email):
    """
    Logs in a manager by checking their credentials.
    """
    manager = Manager.query.filter_by(name=name, ssn=ssn, email=email).first()
    if manager:
        return True, manager
    return False, "Manager not found"

def register_client(name, ssn, email, road, number, city):
    """
    Registers a new client to the database.
    """
    try:
        new_client = Client(name=name, ssn=ssn, email=email)
        db.session.add(new_client)
        db.session.commit()


        new_address = Address(road=road, number=number, city=city)
        db.session.add(new_address)
        db.session.commit()

        new_client_address = ClientAddress(client_id=new_client.id, road=road, number=number, city=city)
        db.session.add(new_client_address)
        db.session.commit()
        return True, new_client
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)

def register_driver(name, road, number, city):
    """
    Registers a new driver to the database.
    """
    try:
        new_address = Address(road=road, number=number, city=city)
        db.session.add(new_address)
        db.session.commit()

        new_driver = Driver(name=name, road=road, number=number, city=city)
        db.session.add(new_driver)
        db.session.commit()
        return True, new_driver
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)