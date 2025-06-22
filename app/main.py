from fastapi import FastAPI, UploadFile, File
from typing import List
import csv
import io
import os

try:
    import openai
except ImportError:
    openai = None

app = FastAPI(title="Ask-and-Retrieve")

documents = []  # simple in-memory store

def embed_text(text: str) -> List[float]:
    """Return embedding vector for text. Requires OPENAI_API_KEY env var."""
    if openai is None:
        raise RuntimeError("openai package not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Upload a CSV file with columns: name, physical_location, file_path"""
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode()))
    for row in reader:
        vector = embed_text(row.get("name", ""))
        documents.append({
            "name": row.get("name"),
            "physical_location": row.get("physical_location"),
            "file_path": row.get("file_path"),
            "embedding": vector,
        })
    return {"count": len(documents)}

@app.post("/query")
async def query(text: str):
    """Query documents using text."""
    vector = embed_text(text)
    # compute cosine similarity
    def cosine(a, b):
        import math
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb)

    if not documents:
        return {"results": []}

    scored = [
        (cosine(vector, doc["embedding"]), doc) for doc in documents
    ]
    scored.sort(key=lambda x: x[0], reverse=True)

    top = [
        {
            "name": s[1]["name"],
            "physical_location": s[1]["physical_location"],
            "file_path": s[1]["file_path"],
            "score": s[0],
        }
        for s in scored[:5]
    ]
    return {"results": top}
