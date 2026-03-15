import os
from app.ingestion import ingest_file
from app.chunking import chunk_text
from app.embeddings import embed_chunks
from app.vectorstore import add_to_vectorstore

RAW_DIR = "data/raw_docs"
PROCESSED_DIR = "data/processed"

def ingest_all_books():
    for filename in os.listdir(RAW_DIR):
        if not filename.endswith(".txt"):
            continue

        print(f"\n=== Processing {filename} ===")

        # 1. Ingest
        processed_path = ingest_file(filename)

        # 2. Load processed text
        with open(processed_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 3. Chunk
        chunks = chunk_text(text)

        # 4. Embed
        embeddings = embed_chunks(chunks)

        # 5. Index
        add_to_vectorstore(chunks, embeddings, filename)

        print(f"Indexed {len(chunks)} chunks from {filename}")

if __name__ == "__main__":
    ingest_all_books()
