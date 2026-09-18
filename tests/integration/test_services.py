"""Integration: real Qdrant server + real Ollama (requires services up)."""
from core.qdrant_factory import get_qdrant_client
from core.providers.ollama_embedder import OllamaEmbedder
from core.providers.ollama_chat import OllamaChat
from core.providers.qdrant_retriever import QdrantRetriever

def test_qdrant_collections_exist():
    c = get_qdrant_client()
    names = {x.name for x in c.get_collections().collections}
    assert "enterprise_rag" in names

def test_ollama_embed_dim():
    v = OllamaEmbedder().embed_query("hello")
    assert len(v) == 1024

def test_ollama_chat_ok():
    assert OllamaChat().healthcheck() is True

def test_qdrant_retriever_returns_chunks():
    chunks = QdrantRetriever(get_qdrant_client(), OllamaEmbedder()).search("What is LangGraph?")
    assert len(chunks) > 0
    assert "text" in chunks[0] and chunks[0]["text"].strip() != ""
