#Contains view functions that handle HTTP requests and define URL endpoints

from flask import render_template, redirect, url_for, flash, request
from rental_app import db
from rental_app.clients import clients_bp
# from rental_app.models import Manager, Car, Driver # Example of how to import models
# from rental_app.clients.forms import AddCarForm, AssignDriverForm   Example of how to import forms
