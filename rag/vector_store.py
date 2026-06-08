import chromadb

_client = None

def get_collection():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path="chroma_store")
    return _client.get_or_create_collection(
        name="logistics_insights",
        metadata={"hnsw:space": "cosine"}, #cosine suits normalized text embedding
    )

