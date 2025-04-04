from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf, extract_skills
from job_matcher import get_job_description, calculate_match_score
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analysis.db'
db = SQLAlchemy(app)

# Create model
class AnalysisHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    match_score = db.Column(db.Float)
    skills_found = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        job_role = request.form.get("job_role", "data_scientist")

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            skills = extract_skills(resume_text)

            job_desc = get_job_description(f"jobs/{job_role}.json")
            job_keywords = job_desc["keywords"]

            match_score = calculate_match_score(resume_text, job_desc)

            matched_skills = list(set(skills) & set(job_keywords))
            missing_skills = list(set(job_keywords) - set(skills))

            # Save to DB
            history = AnalysisHistory(
                filename=file.filename,
                match_score=match_score,
                skills_found=", ".join(skills)
            )
            db.session.add(history)
            db.session.commit()

            # Recent records
            recent_history = AnalysisHistory.query.order_by(AnalysisHistory.id.desc()).limit(5).all()

            return render_template("index.html",
                                   skills=skills,
                                   score=match_score,
                                   matched_count=len(matched_skills),
                                   missing_count=len(missing_skills),
                                   suggestions=missing_skills,
                                   history=recent_history)

    # GET method
    history = AnalysisHistory.query.order_by(AnalysisHistory.id.desc()).limit(5).all()
    return render_template("index.html", skills=None, score=None, history=history)

if __name__ == "__main__":
    app.run(debug=True)
