"""Qdrant vector retriever — payload contract versioned."""
from __future__ import annotations
from qdrant_client.http.models import SearchParams
from core.config import SETTINGS

REQUIRED_PAYLOAD_KEYS = {"repo", "source", "relative_path", "filename", "extension", "chunk_index", "text"}

def payload_to_chunk(payload: dict, score: float = 0.0) -> dict:
    return {
        "repo": payload.get("repo", ""),
        "source": payload.get("source", ""),
        "relative_path": payload.get("relative_path", ""),
        "filename": payload.get("filename", ""),
        "extension": payload.get("extension", ""),
        "chunk_index": payload.get("chunk_index", 0),
        "text": payload.get("text", ""),
        "score": score,
    }

class QdrantRetriever:
    def __init__(self, client, embedder, collection: str | None = None, top_k: int | None = None):
        self.client = client
        self.embedder = embedder
        self.collection = collection or SETTINGS.collection
        self.top_k = top_k or SETTINGS.top_k

    def search(self, query: str) -> list[dict]:
        vec = self.embedder.embed_query(query)
        res = self.client.query_points(
            collection_name=self.collection,
            query=vec,
            limit=self.top_k,
            with_payload=True,
            search_params=SearchParams(hnsw_ef=32, exact=False),
        )
        points = getattr(res, "points", res)
        out: list[dict] = []
        for p in points:
            payload = p.payload or {}
            out.append(payload_to_chunk(payload, score=getattr(p, "score", 0.0)))
        return out
