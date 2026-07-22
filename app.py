from flask import Flask, render_template, request
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import preprocess_resume_text

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
    processed_tokens = preprocess_resume_text(extracted_text)

    return f"""
    <h2>File '{file.filename}' uploaded successfully!</h2>
    <h3>Raw Extracted Text:</h3>
    <pre>{extracted_text}</pre>
    <h3>Processed Tokens:</h3>
    <pre>{processed_tokens}</pre>
    """

if __name__ == '__main__':
    app.run(debug=True)