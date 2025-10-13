import os
import time

import pytest
import requests


def wait_for_ready(url: str, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(f"{url}/readyz", timeout=2)
            if resp.status_code == 200:
                return
        except requests.RequestException:
            time.sleep(1)
    raise RuntimeError(f"service at {url} did not become ready")


def test_happy_path():
    gateway = os.environ.get("GATEWAY_URL", "http://localhost:8080")
    try:
        wait_for_ready(gateway)
    except RuntimeError as exc:
        pytest.skip(str(exc))

    user_resp = requests.post(
        f"{gateway}/v1/users",
        json={"name": "Test User", "email": "test@example.com"},
        timeout=5,
    )
    user_resp.raise_for_status()
    user_id = user_resp.json()["id"]

    order_resp = requests.post(
        f"{gateway}/v1/orders",
        json={"user_id": user_id, "item": "starter-kit", "quantity": 1},
        timeout=5,
    )
    order_resp.raise_for_status()

    inventory_resp = requests.get(f"{gateway}/v1/inventory", timeout=5)
    inventory_resp.raise_for_status()
    assert any(item["sku"] == "starter-kit" for item in inventory_resp.json())
