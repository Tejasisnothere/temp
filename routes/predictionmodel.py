import os
import pandas as pd
from flask import Blueprint, request, jsonify, render_template, send_file
from routes.aiml import generate_report
from datetime import datetime
from utils.decorators import login_required
# Initialize Flask Blueprint
predmodel = Blueprint("predmodel", __name__)

# Define Upload and Report Directories
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, "reports")
os.makedirs(REPORT_FOLDER, exist_ok=True)

@predmodel.route("/")
@login_required
def model_page():
    return render_template("model.html")

# CSV Input Handling & Report Generation
@predmodel.route("/predict_csv", methods=["POST"])
def predict_csv():
    csv_data = request.form.get("csv_data")

    if not csv_data:
        return jsonify({"error": "No CSV data provided"}), 400

    try:
        # Convert CSV input into list of values
        values = [val.strip() for val in csv_data.split(",")]
        if not values:
            return jsonify({"error": "Empty or invalid CSV data"}), 400
            
        column_names = [f"col_{i+1}" for i in range(len(values))]

        # Generate a unique filename for each request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(UPLOAD_FOLDER, f"data_{timestamp}.xlsx")

        # Create DataFrame & Save to Excel
        df = pd.DataFrame([values], columns=column_names)
        df.to_excel(file_path, index=False)

        # Generate Report
        report_path = generate_report(file_path)
        
        if isinstance(report_path, str) and "Error" in report_path:
            return jsonify({"error": report_path}), 500
            
        return render_template("model.html", report_generated=True)
    
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

# Excel File Upload Handling
@predmodel.route("/predict_excel", methods=["POST"])
def predict_excel():
    file = request.files.get("excel_file")

    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400
        
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({"error": "Only Excel files (.xlsx, .xls) are supported"}), 400

    try:
        # Generate a unique filename for each uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(UPLOAD_FOLDER, f"uploaded_{timestamp}.xlsx")
        file.save(file_path)

        # Generate Report
        report_path = generate_report(file_path)
        
        if isinstance(report_path, str) and "Error" in report_path:
            return jsonify({"error": report_path}), 500
            
        return render_template("model.html", report_generated=True)
    
    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

# Report Download (TXT or PDF)
@predmodel.route("/download/<file_type>")
def download_report(file_type):
    """Allows users to download the generated report."""
    
    if file_type not in ['txt', 'pdf']:
        return jsonify({"error": "Invalid file type. Only txt or pdf allowed."}), 400

    file_path = os.path.join(REPORT_FOLDER, f"generated_report.{file_type}")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "Report not found. Generate a report first."}), 404