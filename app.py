from utils.resume_parser import extract_text_from_pdf
from flask import Flask, render_template, request
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
    return f"""
        <h1>File '{file.filename}' uploaded successfully! </h1>
        <h2>Extracted Text:</h2><p>{extracted_text}</p>
        
        """

if __name__ == '__main__':
    app.run(debug=True)