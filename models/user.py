from . import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    iba = db.Column(db.String(300))  # Optional by default

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash  # Fix this line

    