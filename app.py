from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf, extract_skills
from job_matcher import get_job_description, calculate_match_score

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            skills = extract_skills(resume_text)

            job_desc = get_job_description("jobs/data_scientist.json")
            match_score = calculate_match_score(resume_text, job_desc)

            return render_template("index.html", skills=skills, score=match_score)

    return render_template("index.html", skills=None, score=None)

if __name__ == "__main__":
    app.run(debug=True)
