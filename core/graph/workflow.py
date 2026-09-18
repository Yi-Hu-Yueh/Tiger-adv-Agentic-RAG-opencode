"""Graph workflow state machine (active runtime)."""
from __future__ import annotations
import time
from typing import TYPE_CHECKING
from core.config import SETTINGS
from core.graph.state import AgentState
from core.graph.router import GraphRouter

if TYPE_CHECKING:
    from core.graph.nodes import GraphNodes

class GraphWorkflow:
    """Custom state-machine runtime used by FastAPI (LangGraph adapter is alternative)."""
    def __init__(self, nodes: "GraphNodes", router: GraphRouter | None = None):
        self.nodes = nodes
        self.router = router or GraphRouter()

    def run(self, question: str, chat_history: list[dict] | None = None) -> AgentState:
        t0 = time.time()
        state = AgentState(question=question, chat_history=chat_history or [],
                           memory_enabled=SETTINGS.memory_enabled, memory_window=SETTINGS.memory_window)
        self.nodes.retrieve(state)
        self.nodes.build_memory(state)
        self.nodes.grade(state)
        nxt = self.router.after_grade(state)
        if nxt == "rewrite":
            self.nodes.rewrite(state)
            self.nodes.retrieve(state)
            self.nodes.grade(state)
        self.nodes.generate(state)
        self.nodes.check_hallucination(state)
        nxt2 = self.router.after_check(state)
        if nxt2 == "reflect_rewrite":
            self.nodes.reflect(state)
            if state.rewrite_count < self.router.max_rewrite:
                self.nodes.rewrite(state)
                self.nodes.retrieve(state)
                self.nodes.grade(state)
                self.nodes.generate(state)
                self.nodes.check_hallucination(state)
        self.nodes.build_citations(state)
        state.metadata["total_time"] = round(time.time() - t0, 3)
        state.metadata["steps"] = list(state.metadata.get("timings", {}).keys())
        return state
