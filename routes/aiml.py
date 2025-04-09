import os
import pandas as pd
import google.generativeai as genai
from fpdf import FPDF
import textwrap
from dotenv import load_dotenv

# Load environment variables

# Configure Gemini AI (Use environment variables for safety)

genai.configure(api_key="AIzaSyBOx6nBHj6q6QipKBUKk-diFvs_zUkh5fw")

# Set Directories
UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = os.path.join(UPLOAD_FOLDER, "reports")
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def generate_report(file_path):
    """Reads the uploaded Excel file and generates a pharmaceutical investigation report."""
    
    # Validate file exists
    if not os.path.exists(file_path):
        return "Error: File not found."
    
    try:
        # Load Excel Data
        df = pd.read_excel(file_path)
        if df.empty:
            return "Error: Uploaded file contains no data."

        print(f"📊 Excel loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

        # Always select first row (row_index = 0)
        row_data = df.iloc[0].dropna().to_dict()  # Convert row to dictionary
        
        if not row_data:
            return "Error: No valid data found in the first row."

        # Format Data for Prompt
        formatted_data = "\n".join([f"{key}: {value}" for key, value in row_data.items()])
        
        # Investigation Report Prompt
        prompt = f"""
        You are a pharmaceutical Quality Assurance expert. Based on the provided data, generate a detailed investigation report with the following structure:
        
        1. Deviation Details 
        2. Description
        3. Immediate Actions Taken
        4. Investigation
        5. Root Cause
        6. Corrective and Preventive Actions (CAPA)
        7. Impact
        8. Conclusion
        
        Ensure clear paragraph spacing and professional tone.
        Do NOT include unnecessary symbols or markdown formatting.
        
        **Excel Data for Analysis:**
        {formatted_data}
        """

        # Generate Report using Gemini AI
        print("🧠 Generating report using Gemini Pro... please wait ⏳")
        
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        
        if not response.text:
            return "Error: No response generated from AI model."
            
        report_text = response.text

        # Save Report as Text File
        report_path_txt = os.path.join(REPORTS_FOLDER, "generated_report.txt")
        with open(report_path_txt, "w", encoding="utf-8") as file:
            file.write(report_text)

        # Convert to PDF
        report_path_pdf = os.path.join(REPORTS_FOLDER, "generated_report.pdf")
        convert_text_to_pdf(report_text, report_path_pdf)

        return report_path_pdf
    
    except Exception as e:
        error_msg = f"Error generating report: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def convert_text_to_pdf(text, pdf_path):
    """Converts text report into a properly formatted PDF file."""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "Pharmaceutical Investigation Report", 0, 1, "C")
        pdf.ln(10)
        
        # Add content with proper formatting
        pdf.set_font("Arial", "", 11)
        
        # Process text paragraph by paragraph for better formatting
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            # Check if this is a section header (numbered item)
            if paragraph.strip() and any(f"{i}." in paragraph[:3] for i in range(1, 9)):
                # It's likely a header - make it bold
                pdf.set_font("Arial", "B", 12)
                pdf.multi_cell(0, 10, paragraph)
                pdf.set_font("Arial", "", 11)
            else:
                # Regular paragraph - wrap text to avoid overflow
                lines = textwrap.wrap(paragraph, width=95)
                for line in lines:
                    pdf.multi_cell(0, 5, line)
            
            pdf.ln(5)
        
        # Add footer with date
        pdf.set_y(-20)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, f"Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, "C")
        
        pdf.output(pdf_path)
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False