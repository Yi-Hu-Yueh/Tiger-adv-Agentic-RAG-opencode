"""LangGraph adapter compiles and runs (alternative runtime)."""
from core.bootstrap import build_workflow
from core.langgraph.workflow import build_langgraph_workflow

def test_langgraph_adapter():
    wf = build_workflow()
    lg = build_langgraph_workflow(wf)
    out = lg.invoke({"question": "What is LangGraph?"})
    assert out.get("answer", "").strip() != ""
