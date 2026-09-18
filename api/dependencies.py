"""Workflow cache — active runtime is custom GraphWorkflow (not LangGraph StateGraph)."""
from __future__ import annotations
from functools import lru_cache
from core.bootstrap import build_workflow

@lru_cache(maxsize=1)
def get_workflow():
    return build_workflow()
