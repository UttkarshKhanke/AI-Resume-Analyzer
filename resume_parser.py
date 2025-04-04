import PyPDF2
import re

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

def extract_skills(text):
    keywords = ["python", "sql", "excel", "pandas", "numpy", "machine learning", "data analysis",
                "deep learning", "statistics", "html", "css", "javascript", "react", "node.js",
                "git", "power bi", "data visualization", "reporting"]
    found = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text)]
    return found
