import sys
import os

from app.ingestion import ingest_file
from app.chunking import chunk_text
from app.embeddings import embed_chunks
from app.vectorstore import add_to_vectorstore

PROCESSED_DIR = "data/processed"


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    print("\n=== 🧪 Running Local RAG Pipeline ===")

    # 1. Ingest
    print(f"\n[1] Ingesting: {filename}")
    processed_path = ingest_file(filename)
    processed_filename = os.path.basename(processed_path)
    print(f"Processed file: {processed_filename}")

    # 2. Load processed text
    print("\n[2] Loading processed text...")
    with open(processed_path, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"Loaded {len(text)} characters")

    # 3. Chunk
    print("\n[3] Chunking...")
    chunks = chunk_text(text)
    print(f"Generated {len(chunks)} chunks")
    print("Sample chunk:", chunks[0][:200], "...")

    # 4. Embed
    print("\n[4] Embedding chunks...")
    vectors = embed_chunks(chunks)
    print(f"Generated {len(vectors)} embeddings")
    print("Vector dimension:", len(vectors[0]))

    # 5. Index
    print("\n[5] Indexing into vectorstore...")
    add_to_vectorstore(chunks, vectors, processed_filename)
    print("Indexing complete!")

    print("\n=== ✅ Pipeline Finished Successfully ===")


if __name__ == "__main__":
    main()
