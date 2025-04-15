from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db  # Import db from models package
from models.user import User  # Import User model  
from flask import flash
from config import Config
from routes.auth import auth
from routes.home import home
from routes.predictionmodel import predmodel
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "supersecretkey"  # Required for flashing messages

db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(predmodel, url_prefix="/model")

with app.app_context():
    print("Creating database tables...")
    try:
        # Print database path to confirm it's what you expect
        print(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        # Check if tables exist
        tables = db.metadata.tables.keys()

        print(f"Tables in database: {tables}")
        # Check if any users exist
        users_count = User.query.count()
        print(f"Number of users in database: {users_count}")
        print("Database setup complete!")
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__=="__main__":
    app.run(debug=True)
    