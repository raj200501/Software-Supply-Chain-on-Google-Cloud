"""Demo runner that exercises the gateway emulator."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Tuple

import urllib.request

from .gateway import GatewayConfig, GatewayServer
from .logging import StructuredLogger
from .report import build_report
from .simulator import run_simulation
from .storage import SnapshotStore
from .trace import TraceRecorder
from .policy import PolicyEngine


@dataclass
class DemoResult:
    ok: bool
    details: Dict[str, Any]


def _request(method: str, url: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=5) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def run_demo() -> DemoResult:
    logger = StructuredLogger("demo")
    with tempfile.TemporaryDirectory() as tmpdir:
        trace_path = os.path.join(tmpdir, "trace.jsonl")
        tracer = TraceRecorder(path=trace_path, enabled=True)
        config = GatewayConfig(tracer=tracer, logger=logger)
        server = GatewayServer(config=config)
        host, port = server.start()
        base = f"http://{host}:{port}"
        try:
            user = _request("POST", f"{base}/v1/users", {"name": "Demo", "email": "demo@example.com"})
            order = _request(
                "POST",
                f"{base}/v1/orders",
                {"user_id": user["id"], "item": "starter-kit", "quantity": 1},
            )
            inventory = _request("GET", f"{base}/v1/inventory")
            trace_md = tracer.export_markdown()
        finally:
            server.stop()
        simulation = run_simulation(PolicyEngine.from_env())
        store = SnapshotStore(os.path.join(tmpdir, "snapshot.json"))
        store.save(simulation.snapshot)
        snapshot_loaded = store.load()
        report = build_report(simulation.snapshot, config.metrics, tracer, simulation.decisions)
        result = {
            "user_id": user["id"],
            "order_id": order["id"],
            "inventory": inventory,
            "trace_preview": trace_md.splitlines()[:5],
            "report_preview": report.as_markdown().splitlines()[:10],
            "snapshot_keys": list(snapshot_loaded.keys()),
        }
        return DemoResult(ok=True, details=result)


def main() -> int:
    result = run_demo()
    if result.ok:
        print("DEMO PASS")
        print(json.dumps(result.details, indent=2))
        return 0
    print("DEMO FAIL")
    print(json.dumps(result.details, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
