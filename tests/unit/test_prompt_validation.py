from core.prompts.templates import ANSWER_GENERATOR, DOCUMENT_GRADER
import pytest

def test_prompt_missing_vars():
    with pytest.raises(ValueError):
        ANSWER_GENERATOR.render(question="q")

def test_prompt_renders():
    t = ANSWER_GENERATOR.render(question="q", context="c", memory="m")
    assert "DATA ONLY" in t
    g = DOCUMENT_GRADER.render(question="q", chunk="c")
    assert "yes or no" in g
