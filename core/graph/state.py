"""AgentState — single declaration (fixes duplicate-field bug)."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class AgentState:
    question: str = ""
    queries: list[str] = field(default_factory=list)
    retrieved_chunks: list[dict] = field(default_factory=list)
    filtered_chunks: list[dict] = field(default_factory=list)
    context: str = ""
    memory_context: str = ""
    answer: str = ""
    grounded: bool = False
    hallucination_passed: bool = False
    citations: list[dict] = field(default_factory=list)
    rewrite_count: int = 0
    reflection: str = ""
    chat_history: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    memory_enabled: bool = True
    memory_window: int = 5
