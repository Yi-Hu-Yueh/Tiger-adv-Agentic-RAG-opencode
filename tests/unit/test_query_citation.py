from core.agents.agents import QueryGenerator, CitationGenerator

class FakeChat:
    def invoke(self, prompt: str) -> str:
        return "alternative query about LangGraph"

def test_query_generator_keeps_original_first():
    g = QueryGenerator(FakeChat())
    qs = g.generate("What is LangGraph?")
    assert qs[0] == "What is LangGraph?"
    assert len(qs) <= 2
    assert len(set(qs)) == len(qs)

def test_citation_dedup():
    chunks = [
        {"repo": "A", "relative_path": "x.md", "source": "s", "chunk_index": 1},
        {"repo": "A", "relative_path": "x.md", "source": "s", "chunk_index": 1},
        {"repo": "B", "relative_path": "y.md", "source": "s2", "chunk_index": 2},
    ]
    out = CitationGenerator.build(chunks)
    assert len(out) == 2
