"""Multi-agent scaffolding — runs AFTER retrieval (fixes P0 ordering bug)."""
from __future__ import annotations

class PlannerAgent:
    def plan(self, question: str) -> list[str]:
        return ["researcher", "writer", "reviewer", "verifier"]

class ResearcherAgent:
    def run(self, question: str, chunks: list[dict]) -> dict:
        # Summarize evidence (real work on retrieved chunks)
        texts = [c.get("text", "")[:200] for c in chunks[:3]]
        return {"role": "researcher", "evidence_snippets": len(chunks), "preview": " | ".join(texts)[:500]}

class WriterAgent:
    def run(self, question: str, draft: str) -> dict:
        return {"role": "writer", "draft_len": len(draft)}

class ReviewerAgent:
    def run(self, answer: str) -> dict:
        return {"role": "reviewer", "answer_len": len(answer), "has_content": bool(answer.strip())}

class VerifierAgent:
    def run(self, grounded: bool, citations: list) -> dict:
        return {"role": "verifier", "grounded": grounded, "citations": len(citations)}
