from core.utils.memory import MemoryManager, SessionManager
import pytest

def test_memory_window():
    m = MemoryManager()
    m.add("q1", "a1"); m.add("q2", "a2"); m.add("q3", "a3")
    assert m.size() == 3
    assert len(m.latest(2)) == 2
    m.clear(); assert m.size() == 0

def test_session_dup():
    s = SessionManager()
    s.create("s1")
    with pytest.raises(ValueError):
        s.create("s1")
    s.append("s1", "q", "a")
    assert len(s.get("s1")) == 1
    s.remove("s1")
    assert s.get("s1") == []
