"""Retriever pipeline: multi-query merge + dedup + rerank."""
from __future__ import annotations
from core.config import SETTINGS

def dedup_chunks(chunks: list[dict]) -> list[dict]:
    seen, out = set(), []
    for c in chunks:
        key = (c.get("source", ""), c.get("chunk_index", 0))
        if not c.get("source"):
            key = (c.get("repo", ""), c.get("relative_path", ""), c.get("chunk_index", 0))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out

class RetrieverPipeline:
    def __init__(self, query_generator, retriever, reranker):
        self.query_generator = query_generator
        self.retriever = retriever
        self.reranker = reranker

    def retrieve(self, question: str) -> tuple[list[dict], list[str]]:
        queries = self.query_generator.generate(question)[: SETTINGS.max_queries]
        if not queries:
            queries = [question]
        # Always keep original query first
        if queries[0] != question:
            queries = [question] + [q for q in queries if q != question][: SETTINGS.max_queries - 1]
        merged: list[dict] = []
        for q in queries:
            merged.extend(self.retriever.search(q))
        merged = dedup_chunks(merged)
        merged = self.reranker.rerank(question, merged)
        return merged, queries
