-- Car Rental Database Schema

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS DriverModel;
DROP TABLE IF EXISTS ClientAddress;
DROP TABLE IF EXISTS CreditCard;
DROP TABLE IF EXISTS Rent;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Model;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS Driver;
DROP TABLE IF EXISTS Manager;
DROP TABLE IF EXISTS Address;

CREATE TABLE Manager (
    Name VARCHAR(40),
    SSN INT,
    Email VARCHAR(100),
    PRIMARY KEY(Name)
);

CREATE TABLE Address (
    Road VARCHAR(100),
    Number INT,
    City VARCHAR(50),
    PRIMARY KEY(Road, Number, City)
);

CREATE TABLE Driver (
    Name VARCHAR(100),
    Road VARCHAR(100) NOT NULL,
    Number INT NOT NULL,
    City VARCHAR(50) NOT NULL,
    PRIMARY KEY (Name),
    FOREIGN KEY (Road, Number, City) REFERENCES Address(Road, Number, City)
);

CREATE TABLE Car (
    CarID INT,
    Brand VARCHAR(100),
    PRIMARY KEY(CarID)
);

CREATE TABLE Client (
    Name VARCHAR(40),
    EmailAddress VARCHAR(100),
    PRIMARY KEY(EmailAddress)
);

CREATE TABLE Model (
    ModelID INT,
    ConstructionYear INT,
    Color VARCHAR(40),
    TransmissionType VARCHAR(40),
    CarID INT,
    PRIMARY KEY (ModelID, CarID),
    FOREIGN KEY (CarID) REFERENCES Car(CarID)
);

CREATE TABLE Review (
    ReviewID INT,
    Message VARCHAR(255),
    Rating INT,
    DriverName VARCHAR(100) NOT NULL,
    ClientEmail VARCHAR(100) NOT NULL,
    PRIMARY KEY (ReviewID, DriverName),
    FOREIGN KEY (DriverName) REFERENCES Driver(Name),
    FOREIGN KEY (ClientEmail) REFERENCES Client(EmailAddress)
);

CREATE TABLE Rent (
    RentID INT,
    Date DATE,
    DriverName VARCHAR(100) NOT NULL,
    ClientEmail VARCHAR(100) NOT NULL,
    ModelID INT NOT NULL,
    CarID INT NOT NULL,
    PRIMARY KEY(RentID),
    FOREIGN KEY (DriverName) REFERENCES Driver(Name),
    FOREIGN KEY (ClientEmail) REFERENCES Client(EmailAddress),
    FOREIGN KEY (ModelID, CarID) REFERENCES Model(ModelID, CarID)
);

CREATE TABLE CreditCard (
    CardNumber BIGINT,
    ClientEmail VARCHAR(100) NOT NULL,
    Road VARCHAR(100) NOT NULL,
    Number INT NOT NULL,
    City VARCHAR(50) NOT NULL,
    PRIMARY KEY(CardNumber),
    FOREIGN KEY (ClientEmail) REFERENCES Client(EmailAddress),
    FOREIGN KEY (Road, Number, City) REFERENCES Address(Road, Number, City)
);

CREATE TABLE ClientAddress (
    EmailAddress VARCHAR(100) NOT NULL,
    Road VARCHAR(100) NOT NULL,
    Number INT NOT NULL,
    City VARCHAR(50) NOT NULL,
    FOREIGN KEY (EmailAddress) REFERENCES Client(EmailAddress),
    FOREIGN KEY (Road, Number, City) REFERENCES Address(Road, Number, City),
    PRIMARY KEY(EmailAddress, Road, Number, City)
);

CREATE TABLE DriverModel (
    DriverName VARCHAR(100),
    ModelID INT,
    CarID INT,
    FOREIGN KEY (DriverName) REFERENCES Driver(Name),
    FOREIGN KEY (ModelID, CarID) REFERENCES Model(ModelID, CarID),
    PRIMARY KEY (DriverName, ModelID, CarID)
);

-- Add indexes for performance
CREATE INDEX idx_driver_name ON Driver(Name);
CREATE INDEX idx_client_email ON Client(EmailAddress);
CREATE INDEX idx_car_id ON Car(CarID);
CREATE INDEX idx_model_car ON Model(CarID);