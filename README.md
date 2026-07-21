## Module 2 — Resume Parsing (PDF Text Extraction)

This module adds the ability to extract raw text from uploaded PDF resumes,
using the PyMuPDF library.

### Features
- `utils/resume_parser.py`: reusable, testable text-extraction function
- Handles corrupted/unreadable PDFs gracefully via exception handling
- Extracted text is displayed immediately after upload for verification

### Tech used
PyMuPDF (fitz)

### Known limitations
- Scanned/image-based resumes will not extract any text (requires OCR — future improvement)
- Complex multi-column layouts may produce text in a jumbled reading order
