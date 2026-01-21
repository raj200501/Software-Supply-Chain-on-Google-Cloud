"""Minimal requests-compatible shim for local tests.

This avoids external dependencies in environments without PyPI access.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


class RequestException(Exception):
    pass


@dataclass
class Response:
    status_code: int
    _body: bytes
    headers: Dict[str, Any]

    def json(self) -> Any:
        return json.loads(self._body.decode("utf-8"))

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RequestException(f"HTTP {self.status_code}")


def _request(method: str, url: str, json_payload: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Response:
    data = None
    if json_payload is not None:
        data = json.dumps(json_payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            return Response(status_code=response.status, _body=body, headers=dict(response.headers))
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return Response(status_code=exc.code, _body=body, headers=dict(exc.headers))
    except Exception as exc:  # pragma: no cover - best-effort shim
        raise RequestException(str(exc)) from exc


def get(url: str, timeout: int = 5) -> Response:
    return _request("GET", url, timeout=timeout)


def post(url: str, json: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Response:
    return _request("POST", url, json_payload=json, timeout=timeout)
