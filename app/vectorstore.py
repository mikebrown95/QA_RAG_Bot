import chromadb
from typing import List

CHROMA_DIR = "data/vector_store"

# New Chroma client (correct for 0.5+)
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Create or load collection
vectorstore = client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)

def add_to_vectorstore(chunks: List[str], embeddings: List[List[float]], filename: str):
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    vectorstore.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

def query_vectorstore(query: str, n_results: int = 3):
    results = vectorstore.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
