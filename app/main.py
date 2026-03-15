from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import shutil
import os

# Debug prints
print(">>> MAIN IMPORT START <<<")

# Local modules
from app.ingestion import ingest_file
from app.chunking import chunk_text
from app.embeddings import embed_chunks
from app.vectorstore import add_to_vectorstore, query_vectorstore, vectorstore
from app.llm import build_prompt, call_llama, stream_llama_response
from app.reranker import rerank

print(">>> IMPORTS FINISHED <<<")

RAW_DOCS_DIR = "data/raw_docs"
PROCESSED_DIR = "data/processed"

app = FastAPI(title="Local RAG Bot API")


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG backend is running"}


# -----------------------------
# INGEST ENDPOINT
# -----------------------------
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    raw_path = os.path.join(RAW_DOCS_DIR, file.filename)

    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processed_path = ingest_file(file.filename)
    processed_filename = os.path.basename(processed_path)

    return {
        "filename": file.filename,
        "processed_filename": processed_filename,
        "processed_path": processed_path,
        "status": "processed"
    }


# -----------------------------
# CHUNK ENDPOINT
# -----------------------------
@app.post("/chunk")
def chunk_document(processed_filename: str):
    processed_path = os.path.join(PROCESSED_DIR, processed_filename)

    with open(processed_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    return {
        "processed_filename": processed_filename,
        "num_chunks": len(chunks),
        "chunks_preview": chunks[:3]
    }


# -----------------------------
# EMBEDDING ENDPOINT
# -----------------------------
@app.get("/embed")
def embed_document(processed_filename: str):
    processed_path = os.path.join(PROCESSED_DIR, processed_filename)

    with open(processed_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    vectors = embed_chunks(chunks)

    return {
        "processed_filename": processed_filename,
        "num_chunks": len(chunks),
        "vector_dim": len(vectors[0]),
        "sample_vector": vectors[0][:10]
    }


# -----------------------------
# INDEX ENDPOINT
# -----------------------------
@app.post("/index")
def index_document(processed_filename: str):
    processed_path = os.path.join(PROCESSED_DIR, processed_filename)

    with open(processed_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)

    add_to_vectorstore(chunks, embeddings, processed_filename)

    return {
        "processed_filename": processed_filename,
        "chunks_indexed": len(chunks),
        "status": "indexed"
    }


# -----------------------------
# SEARCH ENDPOINT
# -----------------------------
@app.get("/search")
def search(query: str, n_results: int = 3):
    return query_vectorstore(query, n_results)


# -----------------------------
# ASK ENDPOINT (RAG)
# -----------------------------
class AskRequest(BaseModel):
    query: str
    n_results: int = 8


@app.post("/ask")
def ask(request: AskRequest):
    query = request.query

    results = vectorstore.query(
        query_texts=[query],
        n_results=20
    )

    chunks = results["documents"][0]
    reranked_chunks = rerank(query, chunks, top_k=5)

    prompt = build_prompt(query, reranked_chunks)
    answer = call_llama(prompt)

    return {
        "query": query,
        "chunks_used": len(reranked_chunks),
        "answer": answer
    }


# -----------------------------
# STREAMING CHAT ENDPOINT
# -----------------------------
class ChatRequest(BaseModel):
    query: str


@app.post(
    "/chat_stream",
    response_class=StreamingResponse,
    summary="Stream chat responses token-by-token"
)
def chat_stream(request: ChatRequest):
    """Streams LLM responses using retrieved + reranked context."""

    print(">>> ENTERED CHAT_STREAM FUNCTION <<<")

    query = request.query

    # FIX: Use Chroma's native query() instead of similarity_search()
    results = vectorstore.query(
        query_texts=[query],
        n_results=20
    )

    chunks = results["documents"][0]

    reranked = rerank(query, chunks, top_k=5)
    context = "\n\n".join(reranked)

    prompt = f"""
You are a helpful assistant. Use ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    return StreamingResponse(
        stream_llama_response(prompt),
        media_type="text/event-stream"
    )


# Debug: print all routes
print(">>> ROUTES LOADED:")
for route in app.routes:
    print(route.path)
