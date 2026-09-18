from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_shape():
    r = client.get("/health")
    assert r.status_code == 200
    d = r.json()
    assert d["workflow"] == "ready"
    assert d["qdrant_mode"] == "server"
    assert "ollama_chat" in d and "ollama_embed" in d

def test_chat_contract():
    r = client.post("/chat", json={"question": "What is LangGraph?"})
    assert r.status_code == 200
    d = r.json()
    assert d["answer"].strip() != ""
    assert "grounded" in d and "citations" in d

def test_batch_contract():
    r = client.post("/chat/batch", json={"questions": ["What is LangGraph?", "What is LangChain?"]})
    assert r.status_code == 200
    assert len(r.json()["results"]) == 2

def test_stream_contract():
    r = client.post("/chat/stream", json={"question": "What is LangGraph?"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/plain")
    assert len(r.text.strip()) > 0
