from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
email_cache = []

def check_duplicate(email_text: str):
    global email_cache
    email_cache.append(email_text)

    if len(email_cache) > 1: #check if there is more than 1 email in cache.
        tfidf_matrix = vectorizer.fit_transform(email_cache)
        similarity_matrix = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])

        if len(similarity_matrix[0]) > 0 and max(similarity_matrix[0]) > 0.9:
            return True, f"Similar email found with similarity {max(similarity_matrix[0])}"
        else:
            return False, None
    else: #if only 1 email, then it is not a duplicate.
        return False, None