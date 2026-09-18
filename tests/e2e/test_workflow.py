"""E2E full workflow — mirrors README acceptance criteria."""
from core.bootstrap import build_workflow

def test_workflow():
    wf = build_workflow()
    state = wf.run("What is LangGraph and how does it support agentic workflows?")
    assert state.answer != ""
    assert state.hallucination_passed is True
    assert len(state.citations) > 0
    assert state.grounded is True
