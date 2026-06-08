from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed(texts):
    """Accepts a string or list of strings, returns numpy array(s)."""
    return get_model().encode(texts, convert_to_numpy=True)

