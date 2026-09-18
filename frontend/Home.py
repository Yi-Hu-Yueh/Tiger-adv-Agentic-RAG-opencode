"""Tiger Agentic RAG — Streamlit home."""
import streamlit as st
import requests

st.title("Tiger Agentic RAG")
q = st.text_input("Question", "What is LangGraph and how does it support agentic workflows?")
if st.button("Chat"):
    try:
        r = requests.post("http://127.0.0.1:8000/chat", json={"question": q}, timeout=300)
        d = r.json()
        st.write(d.get("answer", ""))
        st.write(f"grounded={d.get('grounded')}")
        st.json(d.get("citations", []))
    except Exception as e:
        st.error(str(e))
