import os
import fitz  # PyMuPDF
import docx2txt

RAW_DOCS_DIR = "data/raw_docs"
PROCESSED_DIR = "data/processed"


def load_pdf(path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def load_docx(path: str) -> str:
    """Extract text from a DOCX file."""
    return docx2txt.process(path)


def load_txt(path: str) -> str:
    """Load plain text files."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize_text(text: str) -> str:
    """Basic cleanup: strip whitespace, collapse multiple newlines."""
    cleaned = text.replace("\r", "").strip()
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned


def ingest_file(filename: str) -> str:
    """Load, extract, normalize, and save processed text."""
    raw_path = os.path.join(RAW_DOCS_DIR, filename)

    if filename.lower().endswith(".pdf"):
        text = load_pdf(raw_path)
    elif filename.lower().endswith(".docx"):
        text = load_docx(raw_path)
    elif filename.lower().endswith(".txt"):
        text = load_txt(raw_path)
    else:
        raise ValueError("Unsupported file type")

    text = normalize_text(text)

    # Save processed text
    processed_path = os.path.join(PROCESSED_DIR, filename + ".txt")
    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(text)

    return processed_path
