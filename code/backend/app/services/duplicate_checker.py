from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
email_cache = {}

def check_duplicate(email_text: str):
    """Checks if an email is a duplicate based on semantic similarity."""
    email_embedding = model.encode(email_text, convert_to_tensor=True)
    
    for existing_email, embedding in email_cache.items():
        similarity = util.pytorch_cos_sim(email_embedding, embedding).item()
        if similarity > 0.9:
            return True, f"Similar to {existing_email} with score {similarity}"
    
    email_cache[email_text] = email_embedding
    return False, None
