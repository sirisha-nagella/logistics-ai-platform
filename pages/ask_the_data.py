import streamlit as st

from rag.vector_store import get_collection

st.header("🤖 Ask the Data")
st.caption(
    "Ask a question about the business insights. Answers are generated from a "
    "precomputed knowledge base and are not affected by the dashboard filters."
)

with st.form("ask_the_data"):
    question = st.text_input(
        "Your question",
        placeholder="e.g. Which country generates the most revenue?"
    )
    submitted = st.form_submit_button("Ask")

if submitted and question.strip():
    # On a fresh deploy chroma_store/ is empty — build the index on first use.
    if get_collection().count() == 0:
        with st.spinner("Building knowledge index..."):
            from scripts.load_knowledge_base import main as build_index
            build_index()

    # Lazy import so the models only load when a question is actually asked.
    from rag.pipeline import answer_question
    with st.spinner("Thinking..."):
        answer, results = answer_question(question)

    st.success(answer)
    with st.expander(f"Sources ({len(results)})"):
        for doc, distance in results:
            st.markdown(f"- `{distance:.3f}` — {doc}")
