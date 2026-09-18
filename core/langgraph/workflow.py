"""LangGraph alternative runtime — experimental, NOT used by FastAPI default path.
Active runtime is core.graph.workflow.GraphWorkflow (see core/bootstrap.py).
This adapter delegates to the same GraphNodes to avoid duplicated business logic.
"""
from __future__ import annotations
from typing import TypedDict
from core.graph.state import AgentState

class LGState(TypedDict, total=False):
    question: str
    answer: str
    grounded: bool
    citations: list

def build_langgraph_workflow(graph_workflow):
    """Wrap active GraphWorkflow as a LangGraph StateGraph."""
    from langgraph.graph import StateGraph, END
    g = StateGraph(LGState)

    def run_node(state: LGState) -> LGState:
        res = graph_workflow.run(state.get("question", ""))
        return {"answer": res.answer, "grounded": res.grounded, "citations": res.citations, "question": res.question}

    g.add_node("run", run_node)
    g.set_entry_point("run")
    g.add_edge("run", END)
    return g.compile()
