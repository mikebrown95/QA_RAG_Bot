from sentence_transformers import CrossEncoder

# Load once at startup
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list[str], top_k: int = 5):
    """
    Rerank retrieved chunks using a cross-encoder.
    Returns the top_k most relevant chunks.
    """
    # Prepare pairs
    pairs = [(query, chunk) for chunk in chunks]

    # Get relevance scores
    scores = reranker.predict(pairs)

    # Sort chunks by score (descending)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

    # Return only the text of the top_k chunks
    return [chunk for chunk, score in ranked[:top_k]]
