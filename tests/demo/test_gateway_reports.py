import json
import os
import urllib.request


def _request(method, url):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode("utf-8")
    return resp.status, json.loads(body)


def test_metrics_endpoint():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("GET", f"{base}/v1/metrics")
    assert status == 200
    assert "http_get" in payload or "http_post" in payload


def test_traces_endpoint():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("GET", f"{base}/v1/traces")
    assert status == 200
    assert isinstance(payload, list)


def test_report_endpoint():
    base = os.environ["GATEWAY_URL"]
    status, payload = _request("GET", f"{base}/v1/report")
    assert status == 200
    assert "report" in payload
    assert "Demo Report" in payload["report"]
