"""High-level agents — thin wrappers over providers + prompts."""
from __future__ import annotations
from core.prompts.templates import (
    ANSWER_GENERATOR, DOCUMENT_GRADER, HALLUCINATION_CHECKER,
    QUERY_REWRITE, QUERY_GENERATE,
)

def _yes(text: str) -> bool:
    return text.strip().lower().startswith("yes")

class QueryGenerator:
    def __init__(self, chat): self.chat = chat
    def generate(self, question: str) -> list[str]:
        qs = [question.strip()]
        if not qs[0]:
            return qs
        try:
            alt = self.chat.invoke(QUERY_GENERATE.render(question=question)).strip().splitlines()[0].strip()
            if alt and alt.lower() != qs[0].lower():
                qs.append(alt)
        except Exception:
            pass
        return qs[:2]

class QueryRewriter:
    def __init__(self, chat): self.chat = chat
    def rewrite(self, question: str) -> str:
        try:
            return self.chat.invoke(QUERY_REWRITE.render(question=question)).strip().splitlines()[0].strip() or question
        except Exception:
            return question

class DocumentGrader:
    def __init__(self, chat): self.chat = chat
    def grade(self, question: str, chunk: dict) -> bool:
        try:
            out = self.chat.invoke(DOCUMENT_GRADER.render(question=question, chunk=chunk.get("text", "")[:2000]))
            return _yes(out)
        except Exception:
            return True
    def batch(self, question: str, chunks: list[dict]) -> list[dict]:
        return [c for c in chunks if self.grade(question, c)]

class AnswerGenerator:
    def __init__(self, chat): self.chat = chat
    def generate(self, question: str, context: str, memory: str = "") -> str:
        return self.chat.invoke(ANSWER_GENERATOR.render(question=question, context=context, memory=memory or "(none)"))

class HallucinationChecker:
    def __init__(self, chat): self.chat = chat
    def check(self, context: str, answer: str) -> bool:
        if not answer.strip() or answer.strip() == "I don't know.":
            return True
        try:
            out = self.chat.invoke(HALLUCINATION_CHECKER.render(context=context[:6000], answer=answer[:3000]))
            return _yes(out)
        except Exception:
            return True

class CitationGenerator:
    @staticmethod
    def build(chunks: list[dict]) -> list[dict]:
        seen, out = set(), []
        for c in chunks:
            key = (c.get("repo", ""), c.get("relative_path", ""), c.get("chunk_index", 0))
            if key in seen:
                continue
            seen.add(key)
            out.append({"repo": c.get("repo", ""), "path": c.get("relative_path", ""), "source": c.get("source", ""), "chunk_index": c.get("chunk_index", 0)})
        return out

class ReflectionAgent:
    def __init__(self, chat): self.chat = chat
    def reflect(self, question: str, answer: str) -> str:
        try:
            return self.chat.invoke(f"Briefly reflect on what could improve this answer.\nQ: {question}\nA: {answer}\nReflection:")[:500]
        except Exception:
            return ""
