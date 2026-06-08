from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

_MODEL_NAME = "google/flan-t5-base"
_tokenizer = None
_model = None

def get_generator():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
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
