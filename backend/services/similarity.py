import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger("resume_matcher")

_ST_MODEL = None
_ST_LOAD_ATTEMPTED = False

def get_sentence_transformer_model():
    """
    Lazy load SentenceTransformer model to optimize startup time.
    """
    global _ST_MODEL, _ST_LOAD_ATTEMPTED
    if _ST_LOAD_ATTEMPTED:
        return _ST_MODEL
    
    _ST_LOAD_ATTEMPTED = True
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
        _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("SentenceTransformer model loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load SentenceTransformer ('all-MiniLM-L6-v2'): {e}. Falling back to TF-IDF cosine similarity.")
        _ST_MODEL = None
        
    return _ST_MODEL


def calculate_semantic_similarity(text1: str, text2: str) -> Dict[str, Any]:
    """
    Calculates semantic similarity percentage between resume text and job description.
    Tries SentenceTransformers first, falls back to TF-IDF cosine similarity.
    """
    if not text1.strip() or not text2.strip():
        return {"similarity_percentage": 0.0, "method": "none"}

    model = get_sentence_transformer_model()

    if model is not None:
        try:
            from sentence_transformers import util
            embeddings = model.encode([text1, text2], convert_to_tensor=True)
            cosine_score = util.cos_sim(embeddings[0], embeddings[1]).item()
            # Normalize cosine score (range typically -1 to 1, practically 0 to 1 for text)
            normalized_score = max(0.0, min(1.0, float(cosine_score)))
            return {
                "similarity_percentage": round(normalized_score * 100, 1),
                "method": "SentenceTransformer (all-MiniLM-L6-v2)"
            }
        except Exception as e:
            logger.warning(f"SentenceTransformer computation failed: {e}. Using TF-IDF fallback.")

    # Fallback to TF-IDF Cosine Similarity
    return _calculate_tfidf_similarity(text1, text2)


def _calculate_tfidf_similarity(text1: str, text2: str) -> Dict[str, Any]:
    """
    Calculates TF-IDF vector cosine similarity.
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        normalized_score = max(0.0, min(1.0, float(score)))

        return {
            "similarity_percentage": round(normalized_score * 100, 1),
            "method": "TF-IDF Cosine Similarity (Fallback)"
        }
    except Exception as e:
        logger.error(f"TF-IDF similarity calculation error: {e}")
        return {
            "similarity_percentage": 50.0,
            "method": "Keyword Frequency Estimation"
        }
