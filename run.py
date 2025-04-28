# Application entry point that starts the Flask server

from rental_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)