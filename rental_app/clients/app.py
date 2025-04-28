from flask import Flask, render_template, request
from rental_app.clients.routes import clients_bp  # <-- Use full import!
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 

import webbrowser
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for Flask-WTF
app.register_blueprint(clients_bp, url_prefix='/client')

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()  # Delay opening the browser
    app.run(debug=True)