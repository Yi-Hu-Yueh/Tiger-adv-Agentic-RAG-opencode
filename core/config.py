"""Central config — single source of truth. Built from scratch."""
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    qdrant_mode: str = os.getenv("QDRANT_MODE", "server")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
    qdrant_path: str = os.getenv(
        "QDRANT_PATH",
        "D:/0TIGER/6months/PythonAPIDevelopment/opencode-prjs/Tiger-adv-Agentic-RAG-opencode/data/qdrant-server",
    )
    collection: str = os.getenv("QDRANT_COLLECTION", "enterprise_rag")
    vector_size: int = int(os.getenv("VECTOR_SIZE", "1024"))
    chat_model: str = os.getenv("CHAT_MODEL", "gemma4:e4b")
    embed_model: str = os.getenv("EMBED_MODEL", "bge-m3")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    top_k: int = int(os.getenv("TOP_K", "5"))
    max_queries: int = int(os.getenv("MAX_QUERIES", "2"))
    max_rewrite: int = int(os.getenv("MAX_REWRITE", "2"))
    memory_enabled: bool = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
    memory_window: int = int(os.getenv("MEMORY_WINDOW", "5"))
    reranker_model: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")

SETTINGS = Settings()
