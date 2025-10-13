import os

import pytest
import requests


@pytest.mark.integration
def test_gateway_health():
    url = os.environ.get("GATEWAY_URL", "http://localhost:8080")
    try:
        resp = requests.get(f"{url}/healthz", timeout=5)
    except requests.RequestException as exc:
        pytest.skip(f"gateway not reachable: {exc}")
    assert resp.status_code == 200
