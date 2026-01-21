"""Structured logging utilities for demo services.

Default output is human-friendly text. JSON output is opt-in via
`LOG_FORMAT=json` to keep default behavior stable.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class StructuredLogger:
    """Minimal structured logger supporting text and JSON formats."""

    name: str
    stream: Any = sys.stdout
    json_format: bool = field(default_factory=lambda: os.getenv("LOG_FORMAT") == "json")

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _emit(self, level: str, message: str, **fields: Any) -> None:
        payload: Dict[str, Any] = {
            "timestamp": self._timestamp(),
            "level": level,
            "logger": self.name,
            "message": message,
        }
        payload.update(fields)
        try:
            if self.json_format:
                self.stream.write(json.dumps(payload, sort_keys=True) + "\n")
            else:
                kv = " ".join(f"{k}={v}" for k, v in fields.items())
                line = f"[{payload['timestamp']}] {level.upper()} {self.name}: {message}"
                if kv:
                    line = f"{line} {kv}"
                self.stream.write(line + "\n")
            self.stream.flush()
        except ValueError:
            return

    def info(self, message: str, **fields: Any) -> None:
        self._emit("info", message, **fields)

    def warning(self, message: str, **fields: Any) -> None:
        self._emit("warning", message, **fields)

    def error(self, message: str, **fields: Any) -> None:
        self._emit("error", message, **fields)

    def debug(self, message: str, **fields: Any) -> None:
        if os.getenv("LOG_LEVEL", "info").lower() == "debug":
            self._emit("debug", message, **fields)
