"""LangGraph tools: retriever + calculator (experimental)."""
from __future__ import annotations
from core.utils.tools import calc

def retriever_tool_factory(pipeline):
    from langchain_core.tools import tool
    @tool
    def retriever_tool(query: str) -> str:
        """Search vector DB and return top chunk texts."""
        chunks, _ = pipeline.retrieve(query)
        return "\n\n---\n\n".join(c.get("text", "")[:800] for c in chunks[:5])
    return retriever_tool

def calculator_tool(expression: str) -> float:
    return calc(expression)
