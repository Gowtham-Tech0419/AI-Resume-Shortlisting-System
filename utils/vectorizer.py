from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def create_tfidf_vectors(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer


def display_tfidf_matrix(tfidf_matrix, vectorizer):
    feature_names = vectorizer.get_feature_names_out()
    dense_matrix = tfidf_matrix.toarray()
    df = pd.DataFrame(dense_matrix, columns=feature_names)
    return df