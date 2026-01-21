import json
import os
import urllib.request


def _request(method, url, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
        return resp.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        return exc.code, json.loads(body)


def test_invalid_user_payload():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("POST", f"{base}/v1/users", {"name": "", "email": ""})
    assert status == 400
    assert "invalid user payload" in payload["error"]


def test_invalid_order_payload():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("POST", f"{base}/v1/orders", {"item": "", "quantity": 0})
    assert status == 400
    assert "invalid order payload" in payload["error"]
