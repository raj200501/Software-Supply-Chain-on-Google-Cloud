"""In-process timing metrics registry."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class Timer:
    name: str
    start_time: float = field(default_factory=time.perf_counter)

    def stop(self) -> float:
        return time.perf_counter() - self.start_time


@dataclass
class MetricsRegistry:
    """Collects timing metrics in memory."""

    timings: Dict[str, List[float]] = field(default_factory=dict)

    def start_timer(self, name: str) -> Timer:
        return Timer(name=name)

    def record(self, name: str, duration: float) -> None:
        self.timings.setdefault(name, []).append(duration)

    def summary(self) -> Dict[str, Dict[str, Optional[float]]]:
        summary: Dict[str, Dict[str, Optional[float]]] = {}
        for name, values in self.timings.items():
            if not values:
                summary[name] = {"count": 0, "avg": None, "p95": None}
                continue
            avg = statistics.mean(values)
            p95 = statistics.quantiles(values, n=20)[-1] if len(values) >= 2 else values[0]
            summary[name] = {"count": len(values), "avg": avg, "p95": p95}
        return summary

    def merge(self, other: "MetricsRegistry") -> None:
        for name, values in other.timings.items():
            self.timings.setdefault(name, []).extend(values)

    def iter_metrics(self) -> Iterable[str]:
        return self.timings.keys()
