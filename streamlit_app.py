import streamlit as st
import requests

st.set_page_config(page_title="Local RAG Chat", layout="wide")
st.title("💬 Local RAG Chat (Streaming)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input box
query = st.chat_input("Ask something about your documents...")

if query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # Stream assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        url = "http://localhost:8000/chat_stream"
        payload = {"query": query}

        with requests.post(url, json=payload, stream=True) as r:
            for chunk in r.iter_content(chunk_size=None):
                token = chunk.decode("utf-8")
                full_response += token
                placeholder.write(full_response)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": full_response})
