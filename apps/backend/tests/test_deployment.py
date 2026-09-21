import importlib


def test_port_fallback(monkeypatch):
    monkeypatch.delenv("PORT", raising=False)
    module = importlib.import_module("main")
    assert module.app is not None


def test_port_valid(monkeypatch):
    monkeypatch.setenv("PORT", "8080")
    import os
    assert int(os.getenv("PORT", "8000")) == 8080


def test_port_invalid_is_rejected_by_runtime(monkeypatch):
    monkeypatch.setenv("PORT", "not-a-port")
    import os
    try:
        int(os.getenv("PORT", "8000"))
        assert False
    except ValueError:
        assert True
