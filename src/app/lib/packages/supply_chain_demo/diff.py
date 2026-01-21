"""Snapshot diffing utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DiffResult:
    added: Dict[str, Any]
    removed: Dict[str, Any]
    changed: Dict[str, Any]


def diff_snapshots(before: Dict[str, Any], after: Dict[str, Any]) -> DiffResult:
    added: Dict[str, Any] = {}
    removed: Dict[str, Any] = {}
    changed: Dict[str, Any] = {}
    before_keys = set(before.keys())
    after_keys = set(after.keys())
    for key in after_keys - before_keys:
        added[key] = after[key]
    for key in before_keys - after_keys:
        removed[key] = before[key]
    for key in before_keys & after_keys:
        if before[key] != after[key]:
            changed[key] = {"before": before[key], "after": after[key]}
    return DiffResult(added=added, removed=removed, changed=changed)
