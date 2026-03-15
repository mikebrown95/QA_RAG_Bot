from sentence_transformers import SentenceTransformer
from typing import List
from tqdm import tqdm

# Load model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Convert text chunks into embedding vectors using batching
    and a progress bar to avoid MemoryError on large documents.
    """
    all_vectors = []

    for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding chunks"):
        batch = chunks[i:i + batch_size]
        vectors = model.encode(batch, convert_to_numpy=True)
        all_vectors.extend(vectors.tolist())

    return all_vectors
