from sklearn.metrics.pairwise import cosine_similarity
from utils.vectorizer import create_tfidf_vectors


def calculate_similarity(vector_a, vector_b):
    similarity_matrix = cosine_similarity(vector_a, vector_b)
    return similarity_matrix[0][0]


def vectorize_resume_and_job(resume_cleaned_text, job_cleaned_text):
    documents = [resume_cleaned_text, job_cleaned_text]
    tfidf_matrix, vectorizer = create_tfidf_vectors(documents)

    resume_vector = tfidf_matrix[0]
    job_vector = tfidf_matrix[1]

    return resume_vector, job_vector


def rank_candidates(job_cleaned_text, candidate_texts, candidate_names):
    all_documents = [job_cleaned_text] + candidate_texts
    tfidf_matrix, vectorizer = create_tfidf_vectors(all_documents)

    job_vector = tfidf_matrix[0]
    candidate_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(job_vector, candidate_vectors)[0]

    results = list(zip(candidate_names, scores))
    ranked_results = sorted(results, key=lambda x: x[1], reverse=True)

    return ranked_results