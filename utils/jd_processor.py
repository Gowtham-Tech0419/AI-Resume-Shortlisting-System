import json
import os
from utils.text_cleaner import clean_text
from utils.skill_extractor import get_candidate_skills

JD_STORAGE_PATH = 'data/job_descriptions.json'


def process_job_description(raw_jd_text, title="Untitled Job"):
    cleaned = clean_text(raw_jd_text)
    required_skills = get_candidate_skills(cleaned)

    job_data = {
        "title": title,
        "raw_text": raw_jd_text,
        "cleaned_text": cleaned,
        "required_skills": required_skills
    }

    return job_data

def save_job_description(job_data):
    if os.path.exists(JD_STORAGE_PATH) and os.path.getsize(JD_STORAGE_PATH) > 0:
        with open(JD_STORAGE_PATH, 'r') as file:
            try:
                all_jobs = json.load(file)
            except json.JSONDecodeError:
                all_jobs = []
    else:
        all_jobs = []

    job_data["job_id"] = len(all_jobs) + 1
    all_jobs.append(job_data)

    with open(JD_STORAGE_PATH, 'w') as file:
        json.dump(all_jobs, file, indent=4)

    return job_data["job_id"]