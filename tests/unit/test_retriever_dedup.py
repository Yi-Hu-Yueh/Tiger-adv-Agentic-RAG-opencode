from core.retrievers.retriever_pipeline import dedup_chunks

def test_dedup():
    chunks = [
        {"source": "a", "chunk_index": 1},
        {"source": "a", "chunk_index": 1},
        {"source": "b", "chunk_index": 2},
    ]
    assert len(dedup_chunks(chunks)) == 2
