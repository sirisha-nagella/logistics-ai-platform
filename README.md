# AI-Powered Logistics Pricing & Revenue Intelligence Platform

Enterprise-style logistics analytics platform for shipment pricing, revenue forecasting, explainable AI, and business intelligence.

## Tech Stack
- Python
- Streamlit
- XGBoost
- SHAP
- Plotly
- RAG (sentence-transformers + chromadb + FLAN-T5)
- Docker (later)

## Project Goals
- Revenue forecasting
- Pricing analytics
- Explainable AI
- Logistics KPI dashboard
- AI-powered business insights

## Running the App

All dependencies are pinned in `requirements.txt` and installed into the
project's virtual environment (`venv/`). Always launch from that venv so the
RAG dependencies (sentence-transformers, chromadb, transformers) are available
— a globally-installed `streamlit` will fail with `ModuleNotFoundError`.

```bash
# 1. Build the RAG vector index (one-time, and after editing the knowledge base)
./venv/bin/python -m scripts.load_knowledge_base

# 2. Launch the Streamlit app
./venv/bin/python -m streamlit run app.py
```

The "Ask the Data" section (bottom of the app) answers natural-language
questions about the business insights using the local RAG pipeline.

## Branching Workflow

A simple two-tier flow. `main` is always releasable; `develop` is the
integration branch where features come together.

```
feature/* ──PR──> develop ──PR──> main (release)
```

1. **Branch** every change off `develop`: `git checkout develop && git checkout -b feature/<name>`.
2. **Open a PR into `develop`** when the feature is ready (not into `main`).
3. **Release** by opening a PR from `develop` into `main`, then tag the
   release on `main`.

Keep `develop` in sync after any release so it never falls behind `main`.
