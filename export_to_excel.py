"""
export_to_excel.py

Exports the resume shortlisting system's SQLite database (candidates, jobs,
scores) into a single, multi-sheet Excel workbook for recruiter review.

Usage:
    python export_to_excel.py
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime

DB_PATH = 'database/resume_system.db'
OUTPUT_PATH = f'resume_system_export_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'


def load_table_as_dataframe(connection, query):
    """Runs a SQL query and returns the result as a pandas DataFrame."""
    return pd.read_sql_query(query, connection)


def clean_json_column(df, column_name):
    """
    Converts a column containing JSON-encoded lists (e.g. '["python","sql"]')
    into a readable comma-separated string ('python, sql') for Excel display.
    Leaves empty/NULL values as empty strings rather than crashing.
    """
    def parse_row(value):
        if value is None or value == '':
            return ''
        try:
            skills_list = json.loads(value)
            return ', '.join(skills_list)
        except (json.JSONDecodeError, TypeError):
            return str(value)  # fallback: show raw value rather than fail

    df[column_name] = df[column_name].apply(parse_row)
    return df


def export_database_to_excel():
    connection = sqlite3.connect(DB_PATH)

    # --- Candidates sheet ---
    candidates_df = load_table_as_dataframe(connection, "SELECT * FROM candidates")
    if 'detected_skills' in candidates_df.columns:
        candidates_df = clean_json_column(candidates_df, 'detected_skills')

    # --- Jobs sheet ---
    jobs_df = load_table_as_dataframe(connection, "SELECT * FROM jobs")
    if 'required_skills' in jobs_df.columns:
        jobs_df = clean_json_column(jobs_df, 'required_skills')

    # --- Scores sheet (JOINed for readability: names instead of raw IDs) ---
    scores_query = """
        SELECT
            scores.id AS id,
            candidates.name AS ,
            candidates.predicted_category,
            jobs.title AS title,
            ROUND(scores.match_score * 100, 2) AS match_score_percent
        FROM scores
        JOIN candidates ON scores.candidate_id = candidates.id
        JOIN jobs ON scores.job_id = jobs.id
        ORDER BY jobs.title, match_score_percent DESC
    """
    scores_df = load_table_as_dataframe(connection, scores_query)

    connection.close()

    # --- Write all three DataFrames into one workbook, one sheet each ---
    with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
        candidates_df.to_excel(writer, sheet_name='Candidates', index=False)
        jobs_df.to_excel(writer, sheet_name='Jobs', index=False)
        scores_df.to_excel(writer, sheet_name='Scores (Rankings)', index=False)

    print(f"Export complete: {OUTPUT_PATH}")
    print(f"  Candidates: {len(candidates_df)} rows")
    print(f"  Jobs:       {len(jobs_df)} rows")
    print(f"  Scores:     {len(scores_df)} rows")


if __name__ == '__main__':
    export_database_to_excel()