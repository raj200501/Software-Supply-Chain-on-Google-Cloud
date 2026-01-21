"""Environment diagnostics for the demo toolkit."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Diagnostic:
    name: str
    ok: bool
    details: str


def run_diagnostics() -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []
    diagnostics.append(
        Diagnostic(
            name="python",
            ok=sys.version_info >= (3, 10),
            details=f"Python {platform.python_version()}",
        )
    )
    diagnostics.append(
        Diagnostic(
            name="platform",
            ok=True,
            details=f"{platform.system()} {platform.release()}",
        )
    )
    return diagnostics


def as_text(diagnostics: List[Diagnostic]) -> str:
    lines = ["Doctor Report"]
    for diag in diagnostics:
        status = "OK" if diag.ok else "WARN"
        lines.append(f"- {diag.name}: {status} ({diag.details})")
    return "\n".join(lines)
