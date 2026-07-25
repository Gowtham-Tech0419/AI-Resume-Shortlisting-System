import re
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

PROTECTED_TERMS = {
    'c++': 'cplusplus',
    'c#': 'csharp',
    'node.js': 'nodejs',
    'react.js': 'reactjs',
    'vue.js': 'vuejs',
    'asp.net': 'aspnet',
    '.net': 'dotnet',
    'ci/cd': 'cicd',
}

def protect_special_terms(text):
    for original, placeholder in PROTECTED_TERMS.items():
        text = text.replace(original, ' ' + placeholder + ' ')
    return text

def clean_text(text):
    text = text.lower()
    text = protect_special_terms(text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def tokenize_and_remove_stopwords(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens


def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized


def preprocess_resume_text(raw_text):
    cleaned = clean_text(raw_text)
    tokens = tokenize_and_remove_stopwords(cleaned)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens