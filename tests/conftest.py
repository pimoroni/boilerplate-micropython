import sys
import time
from unittest import mock

import pytest


@pytest.fixture(scope="function", autouse=True)
def micropython():
    """Stand in for the micropython module, where const() is a no-op."""
    sys.modules["micropython"] = mock.MagicMock()
    sys.modules["micropython"].const = lambda x: x
    yield sys.modules["micropython"]
    del sys.modules["micropython"]


@pytest.fixture(scope="function", autouse=True)
def machine():
    sys.modules["machine"] = mock.MagicMock()
    yield sys.modules["machine"]
    del sys.modules["machine"]


@pytest.fixture(scope="function", autouse=True)
def ticks(monkeypatch):
    """Add MicroPython's ticks and sleep functions to CPython's time module.

    Sleeps are no-ops, so timeouts in tests should be short enough not to spin.

    """
    monkeypatch.setattr(time, "ticks_ms", lambda: int(time.monotonic() * 1000), raising=False)
    monkeypatch.setattr(time, "ticks_add", lambda ticks, delta: ticks + delta, raising=False)
    monkeypatch.setattr(time, "ticks_diff", lambda a, b: a - b, raising=False)
    monkeypatch.setattr(time, "sleep_ms", lambda ms: None, raising=False)
    monkeypatch.setattr(time, "sleep_us", lambda us: None, raising=False)
