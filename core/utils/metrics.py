"""Execution trace + metrics."""
from __future__ import annotations
import time
from dataclasses import dataclass, field

@dataclass
class ExecutionTrace:
    spans: dict[str, float] = field(default_factory=dict)
    _start: dict[str, float] = field(default_factory=dict)
    def start(self, name: str): self._start[name] = time.time()
    def end(self, name: str):
        if name in self._start: self.spans[name] = round(time.time() - self._start.pop(name), 3)
    def report(self) -> dict: return dict(self.spans)

@dataclass
class ExecutionMetrics:
    retrieved: int = 0
    filtered: int = 0
    rewrite_count: int = 0
    grounded: bool = False
    total_time: float = 0.0
