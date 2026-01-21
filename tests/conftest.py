import os
import threading
import time
from typing import Optional

import pytest

from supply_chain_demo.gateway import GatewayServer

_server: Optional[GatewayServer] = None


def pytest_sessionstart(session):
    global _server
    if os.getenv("LOCAL_GATEWAY") != "1":
        return
    server = GatewayServer()
    host, port = server.start()
    os.environ["GATEWAY_URL"] = f"http://{host}:{port}"
    _server = server


def pytest_sessionfinish(session, exitstatus):
    global _server
    if _server:
        _server.stop()
        _server = None


@pytest.fixture(autouse=True)
def _wait_for_server():
    if os.getenv("LOCAL_GATEWAY") != "1":
        yield
        return
    deadline = time.time() + 5
    url = os.environ.get("GATEWAY_URL")
    assert url, "GATEWAY_URL not set"
    import urllib.request

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}/readyz", timeout=2) as resp:
                if resp.status == 200:
                    break
        except Exception:
            time.sleep(0.2)
    yield
