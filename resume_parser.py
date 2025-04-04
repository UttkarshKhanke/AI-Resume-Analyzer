import os
import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_skills(text):
    doc = nlp(text)
    skills = []
    skill_keywords = ["python", "java", "sql", "excel", "machine learning",
                      "deep learning", "data analysis", "pandas", "numpy", "html", "css", "javascript"]
    
    for token in doc:
        if token.text.lower() in skill_keywords:
            skills.append(token.text.lower())
    
    return list(set(skills))
