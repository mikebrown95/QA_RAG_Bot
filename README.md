📚 QA RAG Bot — Local Retrieval‑Augmented Generation Over Project Gutenberg Books
A fully local, privacy‑preserving Retrieval‑Augmented Generation (RAG) system that ingests books from Project Gutenberg, chunks and embeds them, stores them in a vector database, and provides streaming, context‑aware answers through a clean Streamlit chat interface.

This project demonstrates end‑to‑end AI engineering skills:

Data ingestion & preprocessing

Chunking & embedding pipelines

Vector database integration (ChromaDB)

Retrieval + reranking

LLM prompt orchestration

Streaming responses

FastAPI backend

Streamlit frontend

Modular, production‑ready architecture

## 🎥 Demo Video

Here is a walkthrough of the QA RAG Bot in action:

https://github.com/mikebrown95/QA_RAG_Bot/blob/main/assets/demo_small.mp4

🚀 Features
📥 Multi‑Book Ingestion
Automatically download and ingest multiple Project Gutenberg books.
Each book is cleaned, chunked, embedded, and indexed into ChromaDB.

🔍 High‑Quality Retrieval
Uses dense embeddings + reranking to surface the most relevant passages.

🧠 Local LLM Integration
Streams responses token‑by‑token for a smooth chat experience.

⚡ FastAPI Backend
A clean API with endpoints for:

ingestion

chunking

embedding

indexing

searching

streaming chat

💬 Streamlit Chat UI
A simple, elegant interface for asking questions across your entire book library.

🔒 100% Local
No cloud services.
No external APIs.
Your data stays on your machine.

🏗️ Architecture
Code
                ┌──────────────────────────┐
                │   Project Gutenberg TXT   │
                └──────────────┬───────────┘
                               ▼
                    ┌──────────────────┐
                    │   Ingestion       │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │     Chunking      │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │    Embeddings     │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │   ChromaDB Index  │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │    Reranker       │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │ LLM (Streaming)   │
                    └──────────────────┘
                               ▼
                    ┌──────────────────┐
                    │ Streamlit UI      │
                    └──────────────────┘
📦 Project Structure

project/
│
├── app/
│   ├── main.py               # FastAPI backend
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── reranker.py
│   ├── llm.py
│   └── utils.py
│
├── frontend/
│   └── streamlit_app.py      # Chat UI
│
├── scripts/
│   ├── ingest_gutenberg.py   # Batch ingestion pipeline
│   └── rebuild_index.py
│
├── data/
│   ├── raw_books/
│   ├── processed/
│   └── chroma/               # Vector database (ignored in Git)
│
├── .gitignore
├── requirements.txt
└── README.md

🛠️ Setup
1. Clone the repository
Code
git clone https://github.com/<your-username>/QA_RAG_Bot.git
cd QA_RAG_Bot
2. Create a virtual environment
Code
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
3. Install dependencies
Code
pip install -r requirements.txt
📚 Ingest Books

Download and index multiple books from Project Gutenberg:

Code
python scripts/ingest_gutenberg.py
This will:

download books

clean them

chunk them

embed them

store them in ChromaDB

🚀 Run the Application
Start the backend
Code
uvicorn app.main:app --reload
Start the Streamlit UI
Code
streamlit run frontend/streamlit_app.py
Your chat interface will open in the browser.

💬 Example Queries
Try asking:

“What does Plato say about justice in The Republic?”

“Summarize Aristotle’s view of virtue.”

“Compare Dostoevsky’s themes across The Idiot and The Brothers Karamazov.”

“What philosophical arguments appear in Book II of The Republic?”

The system retrieves relevant passages, reranks them, and streams a synthesized answer.

🧪 Tech Stack
Component	Technology
Backend	FastAPI
Frontend	Streamlit
Vector DB	ChromaDB
Embeddings	SentenceTransformers
Reranking	Cross‑encoder
LLM	Local Llama model
Deployment	Local environment


🎯 Why This Project Matters
This application demonstrates real AI engineering skills:

building ingestion pipelines

working with embeddings and vector databases

designing retrieval + reranking systems

orchestrating LLM prompts

building streaming interfaces

structuring a production‑ready codebase

It’s a complete, end‑to‑end AI system — not just a notebook demo.

📄 License
MIT License.











