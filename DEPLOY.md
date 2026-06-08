# Deploying to Hugging Face Spaces

This app is fully local (sentence-transformers + ChromaDB + FLAN-T5) — **no API
keys, no card**. The only real requirement is RAM, and HF Spaces' free tier
(16 GB) runs it comfortably.

This `deploy/hf-space` branch carries the HF Space config (the README
frontmatter); `develop`/`main` stay frontmatter-free.

## One-time setup

1. Create a free account at https://huggingface.co.
2. Create a **write** access token: Settings → Access Tokens → New token (write).
3. Create the Space: https://huggingface.co/new-space
   - Owner: you
   - Space name: `logistics-revenue-intelligence`
   - SDK: **Streamlit**
   - Hardware: **CPU basic** (free, 16 GB)
   - Visibility: Public

## Deploy

```bash
cd /Users/jagsiri/projects/logistics-ai-platform

# Add the Space as a git remote (once)
git remote add space https://huggingface.co/spaces/<your-username>/logistics-revenue-intelligence

# Push the deploy branch to the Space's main branch.
# When prompted for a password, paste your HF *write* token.
git push space deploy/hf-space:main
```

The Space builds from `requirements.txt` (~2-4 min; torch is large), then boots.
The first "Ask the Data" question downloads FLAN-T5 (~1 GB) and builds the
ChromaDB index (~30-60 s); subsequent questions are fast. The Space sleeps after
~48 h idle and wakes on the next visit.

## Updating the Space later

After new work merges into `main`:

```bash
git checkout deploy/hf-space
git merge main                       # frontmatter stays on top
git push space deploy/hf-space:main
git checkout develop
```

## Notes

- Pinned to `python_version: "3.12"` in the README frontmatter — every
  dependency has a Linux wheel for 3.12 (verified), so the build needs no
  source compilation.
- `data/supply_chain_data.csv` (~3.6 MB) is pushed and will be public on a
  public Space (it is already in the public GitHub repo).
- `chroma_store/`, `models/`, and `venv/` are gitignored and intentionally not
  pushed.
