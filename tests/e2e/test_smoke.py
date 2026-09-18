"""Import smoke — clean-install verification."""
def test_imports():
    import app, core.bootstrap, core.graph.workflow, core.langgraph.workflow
    assert hasattr(app, "app")
    assert hasattr(core.bootstrap, "build_workflow")
