from scripts.test_retrieval import retrieve # or move retrieve into pipeline.py
from rag.generator import generate_answer

def answer_question(query, k=3):
    results = retrieve(query, k)
    docs = [d for d, _ in results]
    answer = generate_answer(query, docs)
    return answer, results
