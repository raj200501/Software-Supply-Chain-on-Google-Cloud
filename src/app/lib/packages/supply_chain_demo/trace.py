"""Trace recorder with JSONL storage and deterministic exports."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TraceEvent:
    name: str
    timestamp: str
    attributes: Dict[str, Any]


class TraceRecorder:
    """Append-only trace recorder writing JSONL to disk when enabled."""

    def __init__(self, path: Optional[str] = None, enabled: bool = False) -> None:
        self.path = path
        self.enabled = enabled
        self._events: List[TraceEvent] = []

    def record(self, name: str, **attributes: Any) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        event = TraceEvent(name=name, timestamp=timestamp, attributes=attributes)
        self._events.append(event)
        if self.enabled and self.path:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")

    def events(self) -> List[TraceEvent]:
        return list(self._events)

    def export_markdown(self) -> str:
        lines = ["# Trace Report", "", "| Event | Timestamp | Attributes |", "| --- | --- | --- |"]
        for event in self._events:
            attrs = json.dumps(event.attributes, sort_keys=True)
            lines.append(f"| {event.name} | {event.timestamp} | `{attrs}` |")
        return "\n".join(lines) + "\n"

    def export_json(self) -> str:
        payload = [asdict(event) for event in self._events]
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_env(cls) -> "TraceRecorder":
        enabled = bool(int(os.getenv("DEMO_TRACE", "0")))
        path = os.getenv("DEMO_TRACE_PATH", "trace/trace.jsonl")
        return cls(path=path, enabled=enabled)
