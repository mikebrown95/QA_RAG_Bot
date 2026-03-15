from typing import List
from tqdm import tqdm

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """
    Fast, memory-safe chunker for very large text files.
    Includes a progress bar.
    """
    chunks = []
    start = 0
    text_length = len(text)

    # Estimate number of chunks for tqdm
    total_chunks = max(1, text_length // (chunk_size - overlap))

    for _ in tqdm(range(total_chunks), desc="Chunking text"):
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap
        if start >= text_length:
            break
        if start < 0:
            start = 0

    return chunks
