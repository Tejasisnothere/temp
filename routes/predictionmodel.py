import os
from flask import Blueprint, request, jsonify, render_template

predmodel = Blueprint("predmodel", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@predmodel.route("/")
def model_page():
    return render_template("model.html")

# Route for Form Submission
@predmodel.route("/predict", methods=["POST"])
def predict():
    field1 = request.form.get("field1")
    field2 = request.form.get("field2")
    
    if not field1 or not field2:
        return jsonify({"error": "Missing input fields"}), 400
    
    # Process form input (modify as per your ML model)
    return jsonify({"message": "Form processed successfully!", "data": [field1, field2]}), 200

# Route for Comma-Separated Values
@predmodel.route("/predict_csv", methods=["POST"])
def predict_csv():
    csv_data = request.form.get("csv_data")
    
    if not csv_data:
        return jsonify({"error": "No CSV data provided"}), 400
    
    values = [val.strip() for val in csv_data.split(",")]
    
    print(values)

    return render_template("model.html", values=values)

