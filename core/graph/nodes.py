"""Graph nodes — each mutates AgentState + records timing."""
from __future__ import annotations
import time
from core.config import SETTINGS

class GraphNodes:
    def __init__(self, pipeline, rewriter, grader, generator, checker, citation_gen, reflector, planner=None, agents=None):
        self.pipeline = pipeline
        self.rewriter = rewriter
        self.grader = grader
        self.generator = generator
        self.checker = checker
        self.citation_gen = citation_gen
        self.reflector = reflector
        self.planner = planner
        self.agents = agents or {}

    def _mark(self, state, name: str, fn):
        t0 = time.time()
        out = fn()
        state.metadata.setdefault("timings", {})[name] = round(time.time() - t0, 3)
        return out

    def retrieve(self, state):
        def _run():
            chunks, queries = self.pipeline.retrieve(state.question)
            state.retrieved_chunks = chunks
            state.queries = queries
        self._mark(state, "retrieve", _run)
        return state

    def build_memory(self, state):
        def _run():
            if not state.memory_enabled:
                state.memory_context = ""
                return
            hist = state.chat_history[-state.memory_window:] if state.memory_window else []
            state.memory_context = "\n".join(f"Q: {h.get('q','')}\nA: {h.get('a','')}" for h in hist)
        self._mark(state, "build_memory", _run)
        return state

    def rewrite(self, state):
        def _run():
            state.question = self.rewriter.rewrite(state.question)
            state.rewrite_count += 1
        self._mark(state, "rewrite", _run)
        return state

    def grade(self, state):
        def _run():
            state.filtered_chunks = self.grader.batch(state.question, state.retrieved_chunks)
            state.context = "\n\n---\n\n".join(c.get("text", "") for c in state.filtered_chunks[:8])
        self._mark(state, "grade", _run)
        return state

    def generate(self, state):
        def _run():
            if not state.filtered_chunks:
                state.answer = "I don't know."
                return
            state.answer = self.generator.generate(state.question, state.context, state.memory_context)
            if state.reflection:
                state.answer = state.answer
        self._mark(state, "generate", _run)
        return state

    def check_hallucination(self, state):
        def _run():
            ok = self.checker.check(state.context, state.answer)
            state.hallucination_passed = ok
            state.grounded = ok and bool(state.filtered_chunks)
        self._mark(state, "check_hallucination", _run)
        return state

    def reflect(self, state):
        def _run():
            state.reflection = self.reflector.reflect(state.question, state.answer)
        self._mark(state, "reflect", _run)
        return state

    def build_citations(self, state):
        def _run():
            state.citations = self.citation_gen.build(state.filtered_chunks)
            # Multi-agent post-processing on REAL results (correct ordering)
            if self.planner and self.agents:
                plan = self.planner.plan(state.question)
                meta = {}
                if "researcher" in plan and "researcher" in self.agents:
                    meta["researcher"] = self.agents["researcher"].run(state.question, state.filtered_chunks)
                if "writer" in plan and "writer" in self.agents:
                    meta["writer"] = self.agents["writer"].run(state.question, state.answer)
                if "reviewer" in plan and "reviewer" in self.agents:
                    meta["reviewer"] = self.agents["reviewer"].run(state.answer)
                if "verifier" in plan and "verifier" in self.agents:
                    meta["verifier"] = self.agents["verifier"].run(state.grounded, state.citations)
                state.metadata["multi_agent"] = meta
        self._mark(state, "build_citations", _run)
        return state
