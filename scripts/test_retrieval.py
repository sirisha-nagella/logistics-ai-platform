from rag.embedding_model import embed
from rag.vector_store import get_collection

def retrieve(query, k=3):
    q_emb = embed([query])
    results = get_collection().query(
        query_embeddings=q_emb.tolist(),
        n_results=k,
    )
    docs = results["documents"][0]
    distances = results["distances"][0]
    return list(zip(docs, distances))

if __name__ == "__main__":
    for q in [
        "Which country generates the most revenue?",
        "What vendor drives revenue?",
        "What product group dominates revenue?",
    ]:
        print(f"\nQ: {q}")
        for doc, dist in retrieve(q):
            print(f" [{dist:.3f}] {doc}")
