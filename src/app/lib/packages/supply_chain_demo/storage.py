"""Storage helpers for snapshotting demo state."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SnapshotStore:
    path: str

    def save(self, snapshot: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(snapshot, handle, indent=2, sort_keys=True)

    def load(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as handle:
            return json.load(handle)
