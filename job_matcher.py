import json

def get_job_description(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def calculate_match_score(resume_text, job_desc):
    count = 0
    for skill in job_desc["keywords"]:
        if skill in resume_text:
            count += 1
    return round((count / len(job_desc["keywords"])) * 100, 2)
