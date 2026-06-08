import os
import threading

import chromadb

# Absolute path so the store resolves the same way regardless of the working
# directory the app/scripts are launched from.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CHROMA_PATH = os.path.join(_ROOT, "chroma_store")

_COLLECTION_NAME = "logistics_insights"
_COLLECTION_METADATA = {"hnsw:space": "cosine"}  # cosine suits normalized text embeddings

_client = None
_lock = threading.Lock()


def _new_client():
    return chromadb.PersistentClient(path=_CHROMA_PATH)


def get_collection():
    global _client
    with _lock:
        if _client is None:
            _client = _new_client()
        try:
            return _client.get_or_create_collection(
                name=_COLLECTION_NAME,
                metadata=_COLLECTION_METADATA,
            )
        except KeyError:
            # chromadb caches its System in a process-global registry keyed by
            # the persist path. Under Streamlit's runtime that registry can be
            # cleared out from under our cached client, making the lookup raise
            # KeyError(persist_path). Rebuild the client once and retry.
            _client = _new_client()
            return _client.get_or_create_collection(
                name=_COLLECTION_NAME,
                metadata=_COLLECTION_METADATA,
            )
