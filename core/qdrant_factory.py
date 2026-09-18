"""Qdrant shared client factory — avoids multi-client file locks."""
from __future__ import annotations
from functools import lru_cache
from qdrant_client import QdrantClient
from core.config import SETTINGS

@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    if SETTINGS.qdrant_mode == "server":
        return QdrantClient(url=SETTINGS.qdrant_url, timeout=60)
    return QdrantClient(path=SETTINGS.qdrant_path)

def close_qdrant_client() -> None:
    try:
        get_qdrant_client.cache_clear()
    except Exception:
        pass
