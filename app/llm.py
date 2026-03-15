import requests
import json


# ---------------------------------------------------------
# Build Prompt
# ---------------------------------------------------------
def build_prompt(query: str, chunks: list[str]) -> str:
    """
    Build a RAG prompt using reranked chunks.
    """
    context = "\n\n".join(chunks)

    prompt = f"""
You are a helpful assistant. Use ONLY the context below to answer the question.
If the answer is not clearly in the context, say:
"I cannot find the answer in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
    return prompt


# ---------------------------------------------------------
# Non‑Streaming Llama Call
# ---------------------------------------------------------
def call_llama(prompt: str) -> str:
    """
    Calls Ollama Llama3 normally (non‑streaming).
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    data = response.json()

    return data.get("response", "")


# ---------------------------------------------------------
# Streaming Llama Call (for Streamlit)
# ---------------------------------------------------------
def stream_llama_response(prompt: str):
    """
    Streams tokens from Ollama Llama3 as they are generated.
    This is used by the /chat_stream endpoint.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }

    # Stream NDJSON lines from Ollama
    with requests.post(url, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                yield token
