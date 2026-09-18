from core.graph.router import GraphRouter
from core.graph.state import AgentState

def test_router_branches():
    r = GraphRouter(max_rewrite=2)
    s = AgentState(question="q")
    assert r.after_retrieve(s) == "grade"
    s.filtered_chunks = []
    s.rewrite_count = 0
    assert r.after_grade(s) == "rewrite"
    s.rewrite_count = 2
    assert r.after_grade(s) == "generate"
    s.filtered_chunks = [{"text": "x"}]
    assert r.after_grade(s) == "generate"
    s.hallucination_passed = True
    assert r.after_check(s) == "citations"
    s.hallucination_passed = False
    s.rewrite_count = 0
    assert r.after_check(s) == "reflect_rewrite"
    s.rewrite_count = 2
    assert r.after_check(s) == "citations"
