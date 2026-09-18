from core.config import SETTINGS

def test_config_defaults():
    assert SETTINGS.qdrant_mode == "server"
    assert SETTINGS.qdrant_url.startswith("http")
    assert SETTINGS.vector_size == 1024
    assert SETTINGS.collection == "enterprise_rag"
    assert SETTINGS.top_k == 5
