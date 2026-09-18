from core.graph.state import AgentState

def test_state_defaults():
    s = AgentState(question="hi")
    assert s.question == "hi"
    assert s.rewrite_count == 0
    assert s.memory_enabled is True
    assert s.memory_window == 5
    # ensure no duplicate-field crash and mutable defaults are isolated
    a, b = AgentState(), AgentState()
    a.citations.append({"x": 1})
    assert b.citations == []
