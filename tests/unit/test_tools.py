from core.utils.tools import calc
import pytest

def test_calc_ok():
    assert calc("1+2*3") == 7
    assert calc("(2+3)/5") == 1.0

def test_calc_rejects():
    with pytest.raises(ValueError):
        calc("__import__('os').system('x')")
    with pytest.raises(ValueError):
        calc("'hi'")
