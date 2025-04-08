# ✅ Install and import packages
import google.generativeai as genai
import pandas as pd
#from docx import Document
import os
# from google.colab import files  # Uncomment this if you're using Google Colab
def generate_report(file_path):
    genai.configure(api_key="AIzaSyBOx6nBHj6q6QipKBUKk-diFvs_zUkh5fw")
    # ✅ API Key Setup (use environment variable for safety)
    # safer than hardcoding

    # ✅ Upload Excel
    

    # ✅ Load Excel Data
    df = pd.read_excel(file_path)
    print(f"📊 Excel loaded with shape: {df.shape}")

    # ✅ Select Row
    try:
        row_index = int(input(f"🔢 Enter row number to investigate (0 to {len(df)-1}): "))
        if not (0 <= row_index < len(df)):
            raise IndexError("Row index out of range.")
    except (ValueError, IndexError) as e:
        print(f"❌ Invalid input: {e}")
        exit()

    # ✅ Prompt from user
    prompt = """
    You are a pharmaceutical Quality Assurance expert. Based only on the data provided below, generate a professional and detailed investigation report.

    Follow this structure exactly, and write at least 6-10 sentences per section:

    1. Deviation Details  
    2. Description  
    3. Immediate Actions Taken  
    4. Investigation  
    5. Root Cause  
    6. Corrective and Preventive Actions (CAPA)  
    7. Impact  
    8. Conclusion  

    Do NOT use any markdown formatting (such as *bold). Use clear **paragraph spacing* between sections and within sections for readability. Ensure the output is suitable for a clean Word document with no unnecessary symbols.

    Here is the data:
    """

    # ✅ Combine data + prompt
    row_data = df.iloc[row_index].dropna().to_string()
    full_prompt = f"{prompt}\n\nExcel Data:\n{row_data}"

    # ✅ Generate report with Gemini (with error handling)
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    print("🧠 Generating report using Gemini Pro... please wait ⏳")

    try:
        response = model.generate_content(full_prompt)
        report_text = response.text
        print("✅ Report generated!")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        report_text = ""

    # ✅ Display the Report
    print(report_text)

# ✅ Save to Word (Optional)
# if report_text:
#     doc = Document()
#     doc.add_heading("Investigation Report", 0)
#     doc.add_paragraph(report_text)
#     output_filename = "Investigation_Report.docx"
#     doc.save(output_filename)

#     # Uncomment the following line if running on Google Colab
#     # files.download(output_filename)

#     print("📄 Report saved as 'Investigation_Report.docx' and ready to download!")
