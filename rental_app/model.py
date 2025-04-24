from rental_app import db
from datetime import datetime

class Manager(db.Model):
    __tablename__ = 'manager'

    name = db.Column(db.String(40), primary_key=True)
    ssn = db.Column(db.Integer)
    email = db.Column(db.String(100))

    def __repr__(self):
        return f'<Manager {self.name}>'

class Address(db.Model):
    __tablename__ = 'address'
    
    road = db.Column(db.String(100), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), primary_key=True)
    
    drivers = db.relationship('Driver', backref='address_ref', lazy=True)
    credit_cards = db.relationship('CreditCard', backref='address_ref', lazy=True)
    client_addresses = db.relationship('ClientAddress', backref='address_ref', lazy=True)
    
    def __repr__(self):
        return f'<Address {self.road}, {self.number}, {self.city}>'

class Driver(db.Model):
    __tablename__ = 'driver'
    
    name = db.Column(db.String(100), primary_key=True)
    road = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['road', 'number', 'city'],
            ['address.road', 'address.number', 'address.city']
        ),
    )
    
    reviews = db.relationship('Review', backref='driver', lazy=True)
    rents = db.relationship('Rent', backref='driver', lazy=True)
    driver_models = db.relationship('DriverModel', backref='driver', lazy=True)
    
    def __repr__(self):
        return f'<Driver {self.name}>'

class Car(db.Model):
    __tablename__ = 'car'
    
    carid = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    
    models = db.relationship('Model', backref='car', lazy=True)
    
    def __repr__(self):
        return f'<Car {self.carid}>'

class Client(db.Model):
    __tablename__ = 'client'
    
    name = db.Column(db.String(40))
    emailaddress = db.Column(db.String(100), primary_key=True)
    
    reviews = db.relationship('Review', backref='client', lazy=True)
    rents = db.relationship('Rent', backref='client', lazy=True)
    credit_cards = db.relationship('CreditCard', backref='client', lazy=True)
    client_addresses = db.relationship('ClientAddress', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.emailaddress}>'

class Model(db.Model):
    __tablename__ = 'model'
    
    modelid = db.Column(db.Integer, primary_key=True)
    carid = db.Column(db.Integer, db.ForeignKey('car.carid'), primary_key=True)
    constructionyear = db.Column(db.Integer)
    color = db.Column(db.String(40))
    transmissiontype = db.Column(db.String(40))
    
    rents = db.relationship('Rent', backref='model', lazy=True)
    driver_models = db.relationship('DriverModel', backref='model', lazy=True)
    
    def __repr__(self):
        return f'<Model {self.modelid} for Car {self.carid}>'

class Review(db.Model):
    __tablename__ = 'review'
    
    reviewid = db.Column(db.Integer, primary_key=True)
    drivername = db.Column(db.String(100), db.ForeignKey('driver.name'), primary_key=True)
    message = db.Column(db.CHAR)
    rating = db.Column(db.Integer)
    clientemail = db.Column(db.String(100), db.ForeignKey('client.emailaddress'), nullable=False)
    
    def __repr__(self):
        return f'<Review {self.reviewid} for Driver {self.drivername}>'

class Rent(db.Model):
    __tablename__ = 'rent'
    
    rentid = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    drivername = db.Column(db.String(100), db.ForeignKey('driver.name'), nullable=False)
    clientemail = db.Column(db.String(100), db.ForeignKey('client.emailaddress'), nullable=False)
    modelid = db.Column(db.Integer, nullable=False)
    carid = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['modelid', 'carid'],
            ['model.modelid', 'model.carid']
        ),
    )
    
    def __repr__(self):
        return f'<Rent {self.rentid}>'

class CreditCard(db.Model):
    __tablename__ = 'creditcard'
    
    cardnumber = db.Column(db.BigInteger, primary_key=True)
    clientemail = db.Column(db.String(100), db.ForeignKey('client.emailaddress'), nullable=False)
    road = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['road', 'number', 'city'],
            ['address.road', 'address.number', 'address.city']
        ),
    )
    
    def __repr__(self):
        return f'<CreditCard {self.cardnumber}>'

class ClientAddress(db.Model):
    __tablename__ = 'clientaddress'
    
    emailaddress = db.Column(db.String(100), db.ForeignKey('client.emailaddress'), primary_key=True)
    road = db.Column(db.String(100), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['road', 'number', 'city'],
            ['address.road', 'address.number', 'address.city']
        ),
    )
    
    def __repr__(self):
        return f'<ClientAddress {self.emailaddress} at {self.road}>'

class DriverModel(db.Model):
    __tablename__ = 'drivermodel'
    
    drivername = db.Column(db.String(100), db.ForeignKey('driver.name'), primary_key=True)
    modelid = db.Column(db.Integer, primary_key=True)
    carid = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['modelid', 'carid'],
            ['model.modelid', 'model.carid']
        ),
    )
    
    def __repr__(self):
        return f'<DriverModel {self.drivername} - Model {self.modelid}>'