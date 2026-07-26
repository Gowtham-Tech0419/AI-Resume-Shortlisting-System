import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def load_dataset(csv_path='data/resume_dataset.csv'):
    df = pd.read_csv(csv_path)
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
    model = LogisticRegression(max_iter=1000)
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