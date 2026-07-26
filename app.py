from flask import Flask, render_template, request
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text, preprocess_resume_text
from utils.skill_extractor import get_candidate_skills
from utils.jd_processor import process_job_description, save_job_description
from utils.vectorizer import create_tfidf_vectors, display_tfidf_matrix
from utils.similarity_engine import vectorize_resume_and_job, calculate_similarity, rank_candidates
from utils.classifier import load_model, predict_category
from utils.db_manager import insert_candidate, insert_job, insert_score, get_job, get_ranked_candidates_for_job

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    file_path = app.config['UPLOAD_FOLDER'] + '/' + file.filename
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    cleaned_string = clean_text(extracted_text)
    processed_tokens = preprocess_resume_text(extracted_text)
    candidate_skills = get_candidate_skills(cleaned_string)

    return f"""
    <h2>File '{file.filename}' uploaded successfully!</h2>
    <h3>Processed Tokens:</h3>
    <pre>{processed_tokens}</pre>
    <h3>Detected Skills:</h3>
    <pre>{candidate_skills}</pre>
    """

@app.route('/post_job')
def post_job_page():
    return render_template('job_description.html')

@app.route('/submit_jd', methods=['POST'])
def submit_jd():
    job_title = request.form['job_title']
    job_text = request.form['job_description']

    job_data = process_job_description(job_text, title=job_title)
    job_id = save_job_description(job_data)

    return f"""
    <h2>Job '{job_title}' saved successfully! (ID: {job_id})</h2>
    <h3>Required Skills Detected:</h3>
    <pre>{job_data['required_skills']}</pre>
    """
@app.route('/test_vectors')
def test_vectors():
    sample_documents = [
        "python sql docker experience",
        "python java machine learning",
        "sql docker aws kubernetes"
    ]
    tfidf_matrix, vectorizer = create_tfidf_vectors(sample_documents)
    table = display_tfidf_matrix(tfidf_matrix, vectorizer)

    return f"<pre>{table.to_string()}</pre>"

@app.route('/compare/<int:job_id>', methods=['POST'])
def compare_resume_to_job(job_id):
    import json

    file = request.files['resume']
    file_path = app.config['UPLOAD_FOLDER'] + '/' + file.filename
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    resume_cleaned = clean_text(extracted_text)

    with open('data/job_descriptions.json', 'r') as f:
        all_jobs = json.load(f)

    job_record = None
    for job in all_jobs:
        if job['job_id'] == job_id:
            job_record = job
            break

    if job_record is None:
        return f"No job found with ID {job_id}", 404

    resume_vector, job_vector = vectorize_resume_and_job(resume_cleaned, job_record['cleaned_text'])
    score = calculate_similarity(resume_vector, job_vector)

    return f"""
    <h2>Match Score: {round(score * 100, 2)}%</h2>
    <h3>Job: {job_record['title']}</h3>
    <h3>Required Skills: {job_record['required_skills']}</h3>
    
    """
@app.route('/compare_page')
def compare_page():
    return render_template('compare.html')


model, vectorizer = load_model()

print(model)

@app.route('/predict_category', methods=['POST'])
def predict_category_route():
    file = request.files['resume']
    file_path = app.config['UPLOAD_FOLDER'] + '/' + file.filename
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    cleaned = clean_text(extracted_text)

    predicted = predict_category(cleaned, model, vectorizer)

    return f"<h2>Predicted Category: {predicted}</h2>"

from utils.classifier import predict_category


@app.route('/compare_and_save/<int:job_id>', methods=['POST'])
def compare_and_save(job_id):
    job_record = get_job(job_id)
    if job_record is None:
        return f"No job found with ID {job_id}", 404

    file = request.files['resume']
    file_path = app.config['UPLOAD_FOLDER'] + '/' + file.filename
    file.save(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    cleaned = clean_text(extracted_text)
    candidate_skills = get_candidate_skills(cleaned)
    predicted = predict_category(cleaned, model, vectorizer)

    candidate_id = insert_candidate(file.filename, file_path, predicted, candidate_skills)

    resume_vector, job_vector = vectorize_resume_and_job(cleaned, job_record['cleaned_text'])
    score = calculate_similarity(resume_vector, job_vector)

    insert_score(candidate_id, job_id, float(score))

    return f"""
    <h2>Saved! Match Score: {round(score * 100, 2)}%</h2>
    <h3>Predicted Category: {predicted}</h3>
    """


@app.route('/rankings/<int:job_id>')
def rankings(job_id):
    job_record = get_job(job_id)
    if job_record is None:
        return f"No job found with ID {job_id}", 404

    ranked = get_ranked_candidates_for_job(job_id)

    rows_html = ""
    for name, category, score in ranked:
        rows_html += f"<tr><td>{name}</td><td>{category}</td><td>{round(score * 100, 2)}%</td></tr>"

    return f"""
    <h2>Rankings for: {job_record['title']}</h2>
    <table border="1">
        <tr><th>Candidate</th><th>Predicted Category</th><th>Match Score</th></tr>
        {rows_html}
    </table>
    """
    
if __name__ == '__main__':
    app.run(debug=True)