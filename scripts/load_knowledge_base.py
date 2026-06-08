"""Load the business-insights knowledge base into the chromadb vector store.

Reads knowledge_base/business_insights.txt, splits it into one chunk per
insight line (folding the spike bullet list into its header), embeds the
chunks, and performs a full reload of the `logistics_insights` collection.

Run from the repo root:
    python -m scripts.load_knowledge_base
"""

import os

from rag.embedding_model import embed
from rag.vector_store import get_collection

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PATH = os.path.join(ROOT, "knowledge_base", "business_insights.txt")


def load_chunks(path: str = KB_PATH) -> list[str]:
    """Split the knowledge base into one chunk per insight line.

    Blank lines are skipped. A line ending in ':' is treated as a header for
    the bullet list that follows; the bullets are folded into the header so
    they are not embedded as orphan fragments.
    """
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    chunks = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.endswith(":"):
            header = line.rstrip(":").strip()
            bullets = []
            i += 1
            while i < len(lines) and lines[i].strip().startswith("-"):
                bullets.append(lines[i].strip().lstrip("-").strip())
                i += 1
            chunks.append(f"{header}: {', '.join(bullets)}." if bullets else line)
        else:
            chunks.append(line)
            i += 1
    return chunks


def main() -> None:
    chunks = load_chunks()
    print(f"Read {len(chunks)} chunks from {os.path.relpath(KB_PATH, ROOT)}")

    embeddings = embed(chunks).tolist()
    ids = [f"insight_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "business_insights.txt", "index": i} for i in range(len(chunks))]

    collection = get_collection()

    # Full reload: clear existing entries so edited/removed lines do not linger.
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Loaded {len(chunks)} chunks into '{collection.name}' "
        f"(collection now has {collection.count()} documents)."
    )


if __name__ == "__main__":
    main()
