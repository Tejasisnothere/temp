from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import random
import hashlib
from models import db  # Import db from models package
from models.user import User  # Import User model
from werkzeug.security import generate_password_hash, check_password_hash
from utils.decorators import login_required

auth = Blueprint("auth", __name__)

# -------- Signup -------- #
@auth.route("/signuppage", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@auth.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    if password1 != password2:
        flash("Passwords do not match!", "error")
        return redirect(url_for("auth.signup_page"))
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        flash("Username already exists.", "error")
        return redirect(url_for("auth.signup_page"))

    hashed_password = generate_password_hash(password1, method="pbkdf2:sha256")
    new_user = User(username=username, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    session["username"] = username  # Store username in session

    flash("Account created successfully! Now complete IBA signup.", "success")
    
    return redirect(url_for("auth.iba_signup_page"))  # Move to IBA signup

# -------- IBA Signup -------- #
@auth.route("/ibasignuppage", methods=["GET"])
def iba_signup_page():
    return render_template("ibasignup.html")

@auth.route('/get-images-signup', methods=['GET'])
def get_images():
    gen_imgs = generate_fixed_image_links(6)
    return jsonify({"images": gen_imgs})


# -------- Login -------- #
@auth.route("/loginpage", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session["username"] = username
        flash("Login successful! Now complete IBA login.", "success")
        return redirect(url_for("auth.iba_login_page"))  # Move to IBA login
    
    flash("Invalid credentials.", "error")
    return redirect(url_for("auth.login_page"))

# -------- IBA Login -------- #
@auth.route("/iba_loginpage", methods=["GET"])
def iba_login_page():
    return render_template("ibaloginpage.html")

@auth.route('/get-images-login', methods=['GET'])
def get_images_login():
    username = session.get("username")
    
    if not username:
        return jsonify({"error": "User not logged in"}), 401
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_images = generate_fixed_image_links(3)  # Generate 3 new images
    user_iba = user.iba.split(",") if user.iba else []
    user_iba.extend(new_images)

    random.shuffle(user_iba)  # Shuffle images

    return jsonify({"images": user_iba})

@auth.route('/submit-order-login', methods=['POST'])
def submit_order_login():
    username = session.get("username")

    if not username:
        flash("Session expired. Please log in again.", "error")
        return redirect(url_for("auth.iba_login_page"))

    data = request.json
    clicked_order = data.get("order", [])

    if not clicked_order:
        return jsonify({"error": "No order data provided"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    iba_string = ",".join(clicked_order)

    # Normalize comparison
    if iba_string.strip() == user.iba.strip():
        print("sucess")
        return render_template("model.html")  # Final destination
    else:
        flash("Invalid IBA Login. Try again.", "error")
        return redirect(url_for("auth.iba_login_page"))

# -------- Image Generation Helper Function -------- #
def generate_fixed_image_links(n):
    links = []
    for _ in range(n):
        random_number = random.randint(1, 10000)
        unique_hash = hashlib.md5(str(random_number).encode()).hexdigest()[:8]
        fixed_url = f"https://picsum.photos/seed/{unique_hash}/200"
        links.append(fixed_url)
    return links


@auth.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login_page"))
