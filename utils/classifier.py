import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.svm import LinearSVC

import re

PROTECTED_TERMS = {
    'c++': 'cplusplus',
    'c#': 'csharp',
    'f#': 'fsharp',
    'node.js': 'nodejs',
    'react.js': 'reactjs',
    'vue.js': 'vuejs',
    'next.js': 'nextjs',
    'asp.net core': 'aspnet core',
    '.net core': 'dotnet core',
    'objective-c': 'objectivec',
    'a/b testing': 'a b testing',
    'ci/cd': 'ci cd',
    'tcp/ip': 'tcp ip',
    'ui/ux': 'ui ux'
}

def preprocess_text(text):
    """Normalize text consistently across all dataset rows."""
    text = str(text).lower()
    for term, replacement in PROTECTED_TERMS.items():
        text = text.replace(term, replacement)
    # Remove remaining special characters cleanly
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return ' '.join(text.split())

def load_dataset(csv_path='data/resume_dataset.csv'):
    df = pd.read_csv(csv_path)
    df['resume_text'] = df['resume_text'].apply(preprocess_text)
    # Drop any duplicate rows created during merging
    df = df.drop_duplicates(subset=['resume_text']).reset_index(drop=True)
    print(f"Total clean samples loaded: {len(df)}")
    return df



def split_dataset(df, test_size=0.25, random_state=42):
    X = df['resume_text']
    y = df['category']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test

def vectorize_training_data(X_train, X_test):
    vectorizer = TfidfVectorizer()
    X_train_vectors = vectorizer.fit_transform(X_train)
    X_test_vectors = vectorizer.transform(X_test)
    return X_train_vectors, X_test_vectors, vectorizer


def train_naive_bayes(X_train_vectors, y_train):
    model = MultinomialNB()
    model.fit(X_train_vectors, y_train)
    return model


def train_logistic_regression(X_train_vectors, y_train):
    model = LogisticRegression(C=10.0, max_iter=1000, random_state=42)
    model.fit(X_train_vectors, y_train)
    return model

def train_linear_svc(X_train_vectors, y_train):
    model = LinearSVC(C=1.0, random_state=42,max_iter=2000,class_weight='balanced')
    model.fit(X_train_vectors, y_train)
    return model

def evaluate_model(model, X_test_vectors, y_test):
    predictions = model.predict(X_test_vectors)
    accuracy = accuracy_score(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)
    report = classification_report(y_test, predictions, zero_division=0)

    return accuracy, matrix, report


def save_model(model, vectorizer, model_path='models/resume_classifier.pkl'):
    with open(model_path, 'wb') as file:
        pickle.dump({'model': model, 'vectorizer': vectorizer}, file)


def load_model(model_path='models/resume_classifier.pkl'):
    with open(model_path, 'rb') as file:
        saved_data = pickle.load(file)
    return saved_data['model'], saved_data['vectorizer']


def predict_category(resume_text, model, vectorizer):
    resume_vector = vectorizer.transform([resume_text])
    prediction = model.predict(resume_vector)
    return prediction[0]