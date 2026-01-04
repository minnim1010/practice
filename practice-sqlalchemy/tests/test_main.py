# tests/test_main.py

from app.main import add


def test_add():
    """
    Tests the add function.
    """
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
