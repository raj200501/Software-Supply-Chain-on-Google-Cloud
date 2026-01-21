"""Configuration parsing for demo components."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class DemoConfig:
    host: str
    port: int
    policy_enabled: bool
    trace_enabled: bool
    log_format: str

    @classmethod
    def from_env(cls) -> "DemoConfig":
        host = os.getenv("DEMO_HOST", "127.0.0.1")
        port = int(os.getenv("DEMO_PORT", "8080"))
        policy_enabled = bool(int(os.getenv("DEMO_POLICY", "0")))
        trace_enabled = bool(int(os.getenv("DEMO_TRACE", "0")))
        log_format = os.getenv("LOG_FORMAT", "text")
        return cls(
            host=host,
            port=port,
            policy_enabled=policy_enabled,
            trace_enabled=trace_enabled,
            log_format=log_format,
        )

    def as_dict(self) -> Dict[str, str]:
        return {
            "host": self.host,
            "port": str(self.port),
            "policy_enabled": str(self.policy_enabled),
            "trace_enabled": str(self.trace_enabled),
            "log_format": self.log_format,
        }
