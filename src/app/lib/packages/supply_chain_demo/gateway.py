"""Lightweight gateway emulator for local demos and tests."""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Tuple

from .logging import StructuredLogger
from .metrics import MetricsRegistry
from .report import build_report
from .policy import PolicyEngine
from .trace import TraceRecorder
from .validators import validate_order_payload, validate_user_payload
from .workflow import OrderRecord, OrderWorkflow


@dataclass
class GatewayConfig:
    host: str = "127.0.0.1"
    port: int = 0
    policy_engine: PolicyEngine = field(default_factory=PolicyEngine.from_env)
    metrics: MetricsRegistry = field(default_factory=MetricsRegistry)
    tracer: TraceRecorder = field(default_factory=TraceRecorder.from_env)
    logger: StructuredLogger = field(default_factory=lambda: StructuredLogger("demo-gateway"))


@dataclass
class GatewayState:
    users: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    orders: List[Dict[str, Any]] = field(default_factory=list)
    inventory: Dict[str, int] = field(default_factory=lambda: {
        "starter-kit": 10,
        "pro-kit": 4,
        "enterprise-kit": 2,
    })
    lock: threading.Lock = field(default_factory=threading.Lock)


class GatewayServer:
    """HTTP server implementing a subset of the gateway API for local demos."""

    def __init__(self, config: Optional[GatewayConfig] = None) -> None:
        self.config = config or GatewayConfig()
        self.state = GatewayState()
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> Tuple[str, int]:
        handler = self._make_handler()
        self._server = ThreadingHTTPServer((self.config.host, self.config.port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        host, port = self._server.server_address[:2]
        self.config.logger.info("gateway started", host=host, port=port)
        return host, port

    def stop(self) -> None:
        if self._server is None:
            return
        self.config.logger.info("gateway stopping")
        self._server.shutdown()
        self._server.server_close()
        self._server = None
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None

    def _make_handler(self):
        config = self.config
        state = self.state

        def snapshot_state() -> Dict[str, Any]:
            with state.lock:
                return {
                    "users": list(state.users.values()),
                    "orders": list(state.orders),
                    "inventory": dict(state.inventory),
                }

        class GatewayHandler(BaseHTTPRequestHandler):
            def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _parse_body(self) -> Dict[str, Any]:
                length = int(self.headers.get("Content-Length", "0"))
                if length == 0:
                    return {}
                raw = self.rfile.read(length)
                return json.loads(raw.decode("utf-8"))

            def log_message(self, format: str, *args: Any) -> None:
                config.logger.debug("request", path=self.path, detail=format % args)

            def do_GET(self) -> None:  # noqa: N802
                start = config.metrics.start_timer("http_get")
                if self.path in ("/readyz", "/healthz"):
                    config.tracer.record("health_check", path=self.path)
                    self._send_json(HTTPStatus.OK, {"status": "ok"})
                    config.metrics.record("http_get", start.stop())
                    return
                if self.path == "/v1/inventory":
                    with state.lock:
                        items = [
                            {"sku": sku, "quantity": qty}
                            for sku, qty in sorted(state.inventory.items())
                        ]
                    decision = config.policy_engine.evaluate_inventory_snapshot(state.inventory)
                    if not decision.allowed:
                        config.logger.warning("inventory access denied", reason=decision.reason)
                        self._send_json(
                            HTTPStatus.FORBIDDEN,
                            {"error": "inventory access denied", "reason": decision.reason},
                        )
                        config.metrics.record("http_get", start.stop())
                        return
                    config.tracer.record("inventory_list", count=len(items))
                    self._send_json(HTTPStatus.OK, items)
                    config.metrics.record("http_get", start.stop())
                    return
                if self.path == "/v1/metrics":
                    summary = config.metrics.summary()
                    self._send_json(HTTPStatus.OK, summary)
                    config.metrics.record("http_get", start.stop())
                    return
                if self.path == "/v1/traces":
                    events = [event.__dict__ for event in config.tracer.events()]
                    self._send_json(HTTPStatus.OK, events)
                    config.metrics.record("http_get", start.stop())
                    return
                if self.path == "/v1/report":
                    snapshot = snapshot_state()
                    decisions = [config.policy_engine.evaluate_inventory_snapshot(snapshot["inventory"])]
                    report = build_report(snapshot, config.metrics, config.tracer, decisions)
                    self._send_json(HTTPStatus.OK, {"report": report.as_markdown()})
                    config.metrics.record("http_get", start.stop())
                    return
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                config.metrics.record("http_get", start.stop())

            def do_POST(self) -> None:  # noqa: N802
                start = config.metrics.start_timer("http_post")
                if self.path == "/v1/users":
                    payload = self._parse_body()
                    validation = validate_user_payload(payload)
                    if not validation.ok:
                        self._send_json(
                            HTTPStatus.BAD_REQUEST,
                            {"error": "invalid user payload", "reason": validation.message},
                        )
                        config.metrics.record("http_post", start.stop())
                        return
                    email = payload.get("email", "")
                    decision = config.policy_engine.evaluate_user(email)
                    if not decision.allowed:
                        config.logger.warning("user create denied", reason=decision.reason)
                        self._send_json(
                            HTTPStatus.FORBIDDEN,
                            {"error": "user denied", "reason": decision.reason},
                        )
                        config.metrics.record("http_post", start.stop())
                        return
                    user_id = str(uuid.uuid4())
                    with state.lock:
                        state.users[user_id] = {
                            "id": user_id,
                            "name": payload.get("name", ""),
                            "email": email,
                        }
                    config.tracer.record("user_created", user_id=user_id)
                    self._send_json(HTTPStatus.OK, {"id": user_id})
                    config.metrics.record("http_post", start.stop())
                    return
                if self.path == "/v1/orders":
                    payload = self._parse_body()
                    validation = validate_order_payload(payload)
                    if not validation.ok:
                        self._send_json(
                            HTTPStatus.BAD_REQUEST,
                            {"error": "invalid order payload", "reason": validation.message},
                        )
                        config.metrics.record("http_post", start.stop())
                        return
                    sku = payload.get("item", "")
                    quantity = int(payload.get("quantity", 0))
                    decision = config.policy_engine.evaluate_order(sku, quantity)
                    if not decision.allowed:
                        config.logger.warning("order denied", reason=decision.reason)
                        self._send_json(
                            HTTPStatus.FORBIDDEN,
                            {"error": "order denied", "reason": decision.reason},
                        )
                        config.metrics.record("http_post", start.stop())
                        return
                    order_id = str(uuid.uuid4())
                    workflow = OrderWorkflow()
                    workflow_record = OrderRecord(order_id=order_id, sku=sku, quantity=quantity)
                    with state.lock:
                        workflow.run(workflow_record, dict(state.inventory))
                        state.orders.append(
                            {
                                "id": order_id,
                                "user_id": payload.get("user_id"),
                                "sku": sku,
                                "quantity": quantity,
                                "created_at": time.time(),
                                "workflow_state": workflow_record.state.value,
                                "workflow_history": [state.value for state in workflow_record.history],
                            }
                        )
                        state.inventory[sku] = state.inventory.get(sku, 0) - quantity
                    config.tracer.record("order_created", order_id=order_id, sku=sku)
                    self._send_json(HTTPStatus.OK, {"id": order_id})
                    config.metrics.record("http_post", start.stop())
                    return
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                config.metrics.record("http_post", start.stop())

        return GatewayHandler
