from rental_app import create_app, db

app = create_app()
with app.app_context():
    try:
        db.engine.connect()
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {e}")