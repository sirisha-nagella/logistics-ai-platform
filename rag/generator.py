import threading

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

_MODEL_NAME = "google/flan-t5-base"
_tokenizer = None
_model = None
_lock = threading.Lock()

def get_generator():
    global _tokenizer, _model
    # Serialize loading: transformers 5.x materializes weights lazily, and under
    # Streamlit's rerun model two concurrent loads can publish a model whose
    # weights are still on the `meta` device. Hold a lock for the whole load,
    # force full materialization with a warmup pass, and only then publish the
    # singleton so a half-loaded model is never used.
    with _lock:
        if _model is None:
            tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
            model.eval()
            warmup_ids = tokenizer("warm up", return_tensors="pt").input_ids
            model.generate(warmup_ids, max_new_tokens=1)
            _tokenizer, _model = tokenizer, model
    return _tokenizer, _model

def generate_answer(query, retrieved_docs):
    context = "\n".join(retrieved_docs)
    prompt = (
        "Answer the question using only the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    tokenizer, model = get_generator()
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=100)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)
