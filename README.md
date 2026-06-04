# AI-Powered Logistics Pricing & Revenue Intelligence Platform

Enterprise-style logistics analytics platform for shipment pricing, revenue forecasting, explainable AI, and business intelligence.

## Tech Stack
- Python
- Streamlit
- XGBoost
- SHAP
- Plotly
- Docker (later)
- RAG & FAISS (later)

## Project Goals
- Revenue forecasting
- Pricing analytics
- Explainable AI
- Logistics KPI dashboard
- AI-powered business insights

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
