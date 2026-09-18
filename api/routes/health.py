"""GET /health — checks Qdrant + Ollama chat + embedding (fixes incomplete-health P0)."""
from __future__ import annotations
from fastapi import APIRouter
from core.config import SETTINGS
from core.qdrant_factory import get_qdrant_client
from core.providers.ollama_chat import OllamaChat
from core.providers.ollama_embedder import OllamaEmbedder

router = APIRouter()

@router.get("/health")
def health():
    qdrant_ok = False
    ollama_chat_ok = False
    ollama_embed_ok = False
    try:
        c = get_qdrant_client()
        c.get_collections()
        qdrant_ok = True
    except Exception:
        qdrant_ok = False
    try:
        ollama_chat_ok = OllamaChat().healthcheck()
    except Exception:
        ollama_chat_ok = False
    try:
        ollama_embed_ok = OllamaEmbedder().healthcheck()
    except Exception:
        ollama_embed_ok = False
    ok = qdrant_ok and ollama_chat_ok and ollama_embed_ok
    return {
        "status": "ok" if ok else "degraded",
        "workflow": "ready",
        "vectorstore": "connected" if qdrant_ok else "disconnected",
        "qdrant_mode": SETTINGS.qdrant_mode,
        "collection": SETTINGS.collection,
        "ollama_chat": "ok" if ollama_chat_ok else "down",
        "ollama_embed": "ok" if ollama_embed_ok else "down",
    }
