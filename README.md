# Ask-and-Retrieve Prototype

This repo contains a minimal FastAPI backend prototype for the "Ask-and-Retrieve" assistant. It exposes two endpoints:

- `POST /upload` to upload a CSV file with document information.
- `POST /query` to search the uploaded documents using OpenAI embeddings.

Set `OPENAI_API_KEY` in your environment before running.

Run with:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
