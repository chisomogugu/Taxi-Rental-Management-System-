# ----------------------
# MANAGER SERVICES
# ----------------------
# This module contains the actions that can be performed by the manager.
from sqlalchemy.exc import SQLAlchemyError
from rental_app import db
from rental_app.model import Manager, Address, Driver, Car, Model, DriverModel
from rental_app.model import Review, Rent, ClientAddress, CreditCard
from sqlalchemy import func, and_, not_, exists
from datetime import datetime



def exists_manager(name):
    """
    Checks if a manager exists in the database.
    """
    manager = Manager.query.filter_by(name=name).first()
    if manager:
        return True
    return False


