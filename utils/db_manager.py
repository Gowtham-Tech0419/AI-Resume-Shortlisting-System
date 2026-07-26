import sqlite3
import json

DB_PATH = 'database/resume_system.db'


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = get_connection()
    with open('database/schema.sql', 'r') as file:
        schema_sql = file.read()
    connection.executescript(schema_sql)
    connection.commit()
    connection.close()


def insert_candidate(name, resume_path, predicted_category, detected_skills):
    connection = get_connection()
    cursor = connection.cursor()
    skills_json = json.dumps(detected_skills)
    cursor.execute(
        "INSERT INTO candidates (name, resume_path, predicted_category, detected_skills) VALUES (?, ?, ?, ?)",
        (name, resume_path, predicted_category, skills_json)
    )
    connection.commit()
    candidate_id = cursor.lastrowid
    connection.close()
    return candidate_id


def get_candidate(candidate_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return {
        "id": row[0], "name": row[1], "resume_path": row[2],
        "predicted_category": row[3],
        "detected_skills": json.loads(row[4]) if row[4] else []
    }


def insert_job(title, cleaned_text, required_skills):
    connection = get_connection()
    cursor = connection.cursor()
    skills_json = json.dumps(required_skills)
    cursor.execute(
        "INSERT INTO jobs (title, cleaned_text, required_skills) VALUES (?, ?, ?)",
        (title, cleaned_text, skills_json)
    )
    connection.commit()
    job_id = cursor.lastrowid
    connection.close()
    return job_id


def get_job(job_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return {
        "id": row[0], "title": row[1], "cleaned_text": row[2],
        "required_skills": json.loads(row[3]) if row[3] else []
    }


def insert_score(candidate_id, job_id, match_score):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO scores (candidate_id, job_id, match_score) VALUES (?, ?, ?)",
        (candidate_id, job_id, match_score)
    )
    connection.commit()
    score_id = cursor.lastrowid
    connection.close()
    return score_id


def get_ranked_candidates_for_job(job_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT candidates.name, candidates.predicted_category, scores.match_score
        FROM scores
        JOIN candidates ON scores.candidate_id = candidates.id
        WHERE scores.job_id = ?
        ORDER BY scores.match_score DESC
    """, (job_id,))
    results = cursor.fetchall()
    connection.close()
    return results