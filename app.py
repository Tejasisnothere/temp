from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def get_home_page():
    return render_template("home.html")

@app.route("/loginpage")
def get_login_page():
    return render_template("login.html")

@app.route("/signuppage")
def get_signup_page():
    return render_template("signup.html")

@app.route("/model")
def get_model_page():
    return render_template("model.html")

@app.route("/userlogin", methods=["POST"])
def user_login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password )
    except:
        pass
    finally:
        return render_template("login.html")

@app.route("/usersignup", methods=["POST"])
def user_signup():
    try:
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if(password1!=password2):
            return render_template("signup.html", message="Password mismatch")
        else:
            print(username, password1, password2)
            return render_template("login.html", message="User Created Successfully")
    except:
        pass


if __name__ == "__main__":
    app.run(debug=True)