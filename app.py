from flask import Flask, render_template, request
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text, preprocess_resume_text
from utils.skill_extractor import get_candidate_skills
from utils.jd_processor import process_job_description, save_job_description

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

if __name__ == '__main__':
    app.run(debug=True)