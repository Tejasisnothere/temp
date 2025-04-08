from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from config import Config
from models import db
from routes.auth import auth
from routes.home import home

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "supersecretkey"  # Required for flashing messages

db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(home, url_prefix="/")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
