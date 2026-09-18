"""Ollama chat provider via langchain-ollama."""
from __future__ import annotations
from langchain_ollama import ChatOllama
from core.config import SETTINGS

class OllamaChat:
    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or SETTINGS.chat_model
        self.base_url = base_url or SETTINGS.ollama_host
        self._llm = ChatOllama(model=self.model, base_url=self.base_url)

    def invoke(self, prompt: str) -> str:
        return self._llm.invoke(prompt).content

    def healthcheck(self) -> bool:
        try:
            out = self.invoke("ping")
            return isinstance(out, str) and len(out) > 0
        except Exception:
            return False
