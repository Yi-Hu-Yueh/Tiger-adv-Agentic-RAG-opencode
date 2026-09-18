"""Evaluation console."""
import streamlit as st
import requests, json

st.title("Evaluation")
dataset = st.text_input("dataset_name", "default")
raw = st.text_area("dataset JSON", '[{"question": "What is LangGraph?", "expected_answer": "orchestration framework"}]')
if st.button("Run"):
    try:
        items = json.loads(raw)
        r = requests.post(f"http://127.0.0.1:8000/evaluation/run?dataset_name={dataset}", json=items, timeout=600)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))
if st.button("Dashboard"):
    try:
        r = requests.get("http://127.0.0.1:8000/evaluation/dashboard", timeout=30)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))
