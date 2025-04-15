from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session or not session.get("authenticated"):
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)
    return decorated_function
