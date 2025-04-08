

import google.generativeai as genai
import pandas as pd
# from docx import Document
# from google.colab import files

# ✅ API Key Setup
genai.configure(api_key="AIzaSyBOx6nBHj6q6QipKBUKk-diFvs_zUkh5fw")  # Replace with your Gemini API key

# ✅ Upload Excel
uploaded = files.upload()
for fn in uploaded.keys():
    print(f"✅ File '{fn}' uploaded successfully!")
    file_path = fn

# ✅ Load Excel Data
df = pd.read_excel(file_path)
print(f"📊 Excel loaded with shape: {df.shape}")

# ✅ Define Default Prompt
default_prompt = """
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







# ✅ Combine first row of data + prompt
row_data = df.iloc[0].to_string()
full_prompt = f"{default_prompt}\n\nExcel Data:\n{row_data}"

# ✅ Generate report with Gemini
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
print("🧠 Generating report using Gemini Pro... please wait ⏳")
response = model.generate_content(full_prompt)
report_text = response.text
print("✅ Report generated!")

# ✅ Save to Word
doc = Document()
doc.add_heading("Investigation Report", 0)
doc.add_paragraph(report_text)
output_filename = "Investigation_Report.docx"
doc.save(output_filename)
files.download(output_filename)
print("📄 Report saved and ready to download!")