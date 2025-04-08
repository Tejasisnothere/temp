from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import random
import hashlib
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

    
    if username == "admin" and password == "password":
        
        return redirect(url_for("auth.iba_login_page"))
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
    else:
        print(username, password1)

        

        return redirect(url_for("auth.iba_signup_page"))

@auth.route("/ibasignuppage")
def iba_signup_page():
    return render_template("ibasignup.html")

@auth.route("/iba_loginpage")
def iba_login_page():
    return render_template("ibaloginpage.html")




# iba logic


@auth.route('/get-images', methods=['GET'])
def get_images():
    gen_imgs = generate_fixed_image_links(9)
    print(gen_imgs)
    return jsonify({"images": gen_imgs})

@auth.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    print("Clicked Order:", data["order"])
    return jsonify({"message": "Order received"}), 200

def generate_fixed_image_links(n):
    links = []
    for _ in range(n):
        random_number = random.randint(1, 10000)  # Generate a random number
        unique_hash = hashlib.md5(str(random_number).encode()).hexdigest()[:8]  # Create a hash
        fixed_url = f"https://picsum.photos/seed/{unique_hash}/200"  # Use seed-based URL
        links.append(fixed_url)
    return links
