"""Memory + session (in-process, explicit contract)."""
from __future__ import annotations

class MemoryManager:
    def __init__(self): self._hist: list[dict] = []
    def add(self, q: str, a: str) -> None: self._hist.append({"q": q, "a": a})
    def history(self) -> list[dict]: return list(self._hist)
    def latest(self, n: int) -> list[dict]: return list(self._hist[-n:]) if n else []
    def clear(self) -> None: self._hist.clear()
    def size(self) -> int: return len(self._hist)

class SessionManager:
    def __init__(self): self._sessions: dict[str, list[dict]] = {}
    def create(self, sid: str) -> None:
        if sid in self._sessions: raise ValueError("duplicate session")
        self._sessions[sid] = []
    def get(self, sid: str) -> list[dict]: return self._sessions.get(sid, [])
    def append(self, sid: str, q: str, a: str) -> None: self._sessions.setdefault(sid, []).append({"q": q, "a": a})
    def remove(self, sid: str) -> None: self._sessions.pop(sid, None)
    def list(self) -> list[str]: return list(self._sessions.keys())
