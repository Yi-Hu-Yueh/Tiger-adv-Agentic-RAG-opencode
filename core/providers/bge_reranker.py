"""BGE CrossEncoder reranker with lazy load + graceful fallback."""
from __future__ import annotations
from dataclasses import dataclass
from core.config import SETTINGS

@dataclass
class RankedChunk:
    chunk: dict
    score: float

class BGEReranker:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or SETTINGS.reranker_model
        self._model = None
        self._available: bool | None = None

    def _load(self):
        if self._model is not None or self._available is False:
            return self._model
        try:
            from sentence_transformers import CrossEncoder
            # Do NOT force local_files_only; allow download on first use,
            # but never crash runtime if offline.
            self._model = CrossEncoder(self.model_name)
            self._available = True
        except Exception:
            self._available = False
            self._model = None
        return self._model

    def rerank(self, query: str, chunks: list[dict]) -> list[dict]:
        if not chunks:
            return []
        model = self._load()
        if model is None:
            # Fallback: keep original order (Qdrant score order)
            return chunks
        try:
            pairs = [(query, c.get("text", "")) for c in chunks]
            scores = model.predict(pairs)
            ranked = sorted(zip(chunks, scores), key=lambda x: float(x[1]), reverse=True)
            return [c for c, _ in ranked]
        except Exception:
            return chunks
