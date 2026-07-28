from sklearn.metrics.pairwise import cosine_similarity
from utils.vectorizer import create_tfidf_vectors
from utils.db_manager import get_job, get_all_candidates, score_exists, insert_score

def calculate_skill_overlap(required_skills, candidate_skills):
    """
    Computes what fraction of a job's required skills the candidate actually has.
    Returns a value between 0.0 (no overlap) and 1.0 (candidate has every required skill).
    """
    if not required_skills:
        return 0.0

    required_set = set(required_skills)
    candidate_set = set(candidate_skills)

    matched_skills = required_set.intersection(candidate_set)
    return len(matched_skills) / len(required_set)
def compute_scores_for_job(job_id):
    job_record = get_job(job_id)
    all_candidates = get_all_candidates()

    unscored_candidates = [c for c in all_candidates if not score_exists(c['id'], job_id)]

    if not unscored_candidates:
        return

    documents = [job_record['cleaned_text']] + [c['cleaned_text'] for c in unscored_candidates]
    tfidf_matrix, vectorizer = create_tfidf_vectors(documents)

    job_vector = tfidf_matrix[0]
    candidate_vectors = tfidf_matrix[1:]
    text_scores = cosine_similarity(job_vector, candidate_vectors)[0]

    for candidate, text_score in zip(unscored_candidates, text_scores):
        skill_score = calculate_skill_overlap(
            job_record['required_skills'],
            candidate['detected_skills']
        )

        # skill_score IS the headline match — no blending, no dilution
        insert_score(candidate['id'], job_id, float(skill_score), float(text_score))
        
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