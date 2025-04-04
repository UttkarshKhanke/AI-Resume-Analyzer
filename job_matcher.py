from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def get_job_description(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data.get("description", "")

def calculate_match_score(resume_text, job_desc_text):
    vectorizer = CountVectorizer().fit_transform([resume_text, job_desc_text])
    vectors = vectorizer.toarray()
    score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return round(score * 100, 2)
