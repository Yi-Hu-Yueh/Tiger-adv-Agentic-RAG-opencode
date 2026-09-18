from core.providers.qdrant_retriever import payload_to_chunk

def test_payload_contract():
    p = {"repo": "R", "source": "s", "relative_path": "r", "filename": "f", "extension": ".md", "chunk_index": 3, "text": "hello"}
    c = payload_to_chunk(p, score=0.9)
    assert c["repo"] == "R" and c["text"] == "hello" and c["score"] == 0.9

def test_payload_missing_defaults():
    c = payload_to_chunk({}, score=0.0)
    assert c["text"] == "" and c["chunk_index"] == 0
