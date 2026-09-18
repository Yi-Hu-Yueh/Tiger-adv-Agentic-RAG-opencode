"""Ollama embedding provider (bge-m3, 1024 dims)."""
from __future__ import annotations
from langchain_ollama import OllamaEmbeddings
from core.config import SETTINGS

class OllamaEmbedder:
    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or SETTINGS.embed_model
        self.base_url = base_url or SETTINGS.ollama_host
        self._emb = OllamaEmbeddings(model=self.model, base_url=self.base_url)

    def embed_query(self, text: str) -> list[float]:
        return self._emb.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._emb.embed_documents(texts)

    def healthcheck(self) -> bool:
        try:
            v = self.embed_query("healthcheck")
            return isinstance(v, list) and len(v) == SETTINGS.vector_size
        except Exception:
            return False
