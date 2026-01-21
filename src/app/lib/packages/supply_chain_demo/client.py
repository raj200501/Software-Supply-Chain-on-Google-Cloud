"""HTTP client for the demo gateway."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List
import urllib.request


@dataclass
class GatewayClient:
    base_url: str

    def _request(self, method: str, path: str, payload: Dict[str, Any] | None = None) -> Any:
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(f"{self.base_url}{path}", data=data, method=method)
        request.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(request, timeout=5) as response:
            body = response.read().decode("utf-8")
        return json.loads(body)

    def health(self) -> Dict[str, Any]:
        return self._request("GET", "/healthz")

    def ready(self) -> Dict[str, Any]:
        return self._request("GET", "/readyz")

    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        return self._request("POST", "/v1/users", {"name": name, "email": email})

    def create_order(self, user_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/v1/orders",
            {"user_id": user_id, "item": sku, "quantity": quantity},
        )

    def list_inventory(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/v1/inventory")

    def metrics(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/metrics")

    def report(self) -> Dict[str, Any]:
        return self._request("GET", "/v1/report")
