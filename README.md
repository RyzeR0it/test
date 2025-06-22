# Ask-and-Retrieve Prototype

This repo contains a minimal FastAPI backend prototype for the "Ask-and-Retrieve" assistant. It now includes a very basic web interface for uploading a CSV and querying the documents.

Endpoints:

- `POST /upload` – upload a CSV file with document information.
- `POST /query` – search the uploaded documents using OpenAI embeddings.

Set `OPENAI_API_KEY` in your environment before running.

Run with:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/> in your browser. You should see a simple page
that lets you upload a CSV file and run queries. A small sample file
`sample_data.csv` with 50 entries is included for testing.

The interactive API docs are available at `/docs`.
