import json
import os
import urllib.request


def _request(method, url, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode("utf-8")
    return resp.status, json.loads(body)


def test_healthz_endpoint():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("GET", f"{base}/healthz")
    assert status == 200
    assert payload["status"] == "ok"


def test_user_and_order_flow():
    base = os.environ["GATEWAY_URL"]
    status, user = _request(
        "POST",
        f"{base}/v1/users",
        {"name": "Tester", "email": "demo@example.com"},
    )
    assert status == 200
    assert "id" in user

    status, order = _request(
        "POST",
        f"{base}/v1/orders",
        {"user_id": user["id"], "item": "starter-kit", "quantity": 1},
    )
    assert status == 200
    assert "id" in order

    status, inventory = _request("GET", f"{base}/v1/inventory")
    assert status == 200
    assert any(item["sku"] == "starter-kit" for item in inventory)


def test_inventory_decrements():
    base = os.environ["GATEWAY_URL"]
    _, inventory_before = _request("GET", f"{base}/v1/inventory")
    starter = next(item for item in inventory_before if item["sku"] == "starter-kit")

    status, user = _request(
        "POST",
        f"{base}/v1/users",
        {"name": "Stock", "email": "demo@example.com"},
    )
    assert status == 200

    status, _ = _request(
        "POST",
        f"{base}/v1/orders",
        {"user_id": user["id"], "item": "starter-kit", "quantity": 1},
    )
    assert status == 200

    _, inventory_after = _request("GET", f"{base}/v1/inventory")
    starter_after = next(item for item in inventory_after if item["sku"] == "starter-kit")
    assert starter_after["quantity"] == starter["quantity"] - 1
