from flask import Flask, render_template, request, session
import os
from resume_parser import extract_text, extract_skills
from job_matcher import get_job_description, calculate_match_score

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Folder to save uploaded resumes
UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the resumes folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory history list to store recent resume analyses
history = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_role = request.form["job_role"]

        # Initialize session keys
        if "resume_path" not in session:
            session["resume_path"] = None
            session["resume_name"] = None

        # Handle new file upload
        if "resume" in request.files and request.files["resume"].filename:
            file = request.files["resume"]
            if file:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                session["resume_path"] = filepath
                session["resume_name"] = file.filename

        # Ensure a resume is uploaded
        if not session["resume_path"]:
            return "Error: Please upload a resume first."

        # Extract text and skills from resume
        resume_text = extract_text(session["resume_path"])
        print("Extracted Resume Text:\n", resume_text[:1000])  # Debugging
        extracted_skills = extract_skills(resume_text)
        print("Extracted Skills:", extracted_skills)  # Debugging

        # Load job description
        job_desc = get_job_description(f"jobs/{job_role}.json")
        if not job_desc:
            return "Error: Job description file not found."

        job_keywords = job_desc.get("keywords", [])

        # Calculate match score
        match_score = calculate_match_score(resume_text, job_desc)

        # Determine matched and missing skills
        matched_skills = list(set(extracted_skills) & set(job_keywords))
        missing_skills = list(set(job_keywords) - set(extracted_skills))

        # Update history (limit to last 5 entries)
        history.append({
            "filename": session["resume_name"],
            "job_role": job_role.replace("_", " ").title(),
            "match_score": match_score,
            "skills_found": len(matched_skills),
        })
        history[:] = history[-5:]

        return render_template(
            "index.html",
            skills=extracted_skills,
            score=match_score,
            matched_count=len(matched_skills),
            missing_count=len(missing_skills),
            suggestions=missing_skills,
            history=history,
            selected_role=job_role,
        )

    # GET request
    return render_template("index.html", skills=None, score=None, history=history, selected_role=None)

if __name__ == "__main__":
    app.run(debug=True)
