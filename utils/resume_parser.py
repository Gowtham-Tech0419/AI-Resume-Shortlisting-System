import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        text = ""
        # Iterate through each page and extract text
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print("Error extracting text from PDF: {file_path}", e)
        text = ""
    return text