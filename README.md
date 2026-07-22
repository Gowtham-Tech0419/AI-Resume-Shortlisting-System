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
## Module 3 — NLP Preprocessing

This module transforms raw extracted resume text into clean, standardized
word tokens ready for skill extraction and machine learning.

### Pipeline steps
1. Lowercase the text
2. Remove punctuation, numbers, and special symbols
3. Collapse extra whitespace
4. Tokenize into individual words
5. Remove common English stopwords
6. Lemmatize each word to its dictionary base form

### Tech used
NLTK (word_tokenize, stopwords corpus, WordNetLemmatizer)

### Known limitations
- Lemmatizer defaults to noun assumption; verbs may not fully reduce (e.g., "running" stays "running")
- Generic English stopword list; not yet customized with resume-specific filler words
