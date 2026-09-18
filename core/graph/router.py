"""Router rules extracted for unit testing."""
from __future__ import annotations
from core.config import SETTINGS
from core.graph.state import AgentState

class GraphRouter:
    def __init__(self, max_rewrite: int | None = None):
        self.max_rewrite = max_rewrite if max_rewrite is not None else SETTINGS.max_rewrite

    def after_retrieve(self, state: AgentState) -> str:
        return "grade"

    def after_grade(self, state: AgentState) -> str:
        if not state.filtered_chunks and state.rewrite_count < self.max_rewrite:
            return "rewrite"
        return "generate"

    def after_check(self, state: AgentState) -> str:
        if state.hallucination_passed:
            return "citations"
        if state.rewrite_count < self.max_rewrite:
            return "reflect_rewrite"
        return "citations"
