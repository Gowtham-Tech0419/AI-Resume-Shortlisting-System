from utils.vectorizer import create_tfidf_vectors, display_tfidf_matrix

documents = [
    "python sql docker",
    "python java",
    "experience python team",
    "experience team leadership"
]

tfidf_matrix, vectorizer = create_tfidf_vectors(documents)
result_table = display_tfidf_matrix(tfidf_matrix, vectorizer)

print(result_table)