from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint("auth", __name__)

@auth.route("/loginpage", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth.route("/signuppage", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Dummy check (Replace with database validation)
    if username == "admin" and password == "password":
        flash("Login successful!", "success")
        return redirect(url_for("home.home_page"))
    else:
        flash("Invalid credentials. Try again.", "error")
        return redirect(url_for("auth.login_page"))

@auth.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    if password1 != password2:
        flash("Passwords do not match!", "error")
        return redirect(url_for("auth.signup_page"))

    flash("Account created successfully!", "success")
    return redirect(url_for("auth.login_page"))
