"""Generate human-readable reports from demo state."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List

from .metrics import MetricsRegistry
from .plugins import PluginManager, InventoryAlertPlugin, OrderSummaryPlugin
from .policy import PolicyDecision
from .trace import TraceRecorder


@dataclass
class ReportSection:
    title: str
    body: str


@dataclass
class DemoReport:
    sections: List[ReportSection]

    def as_markdown(self) -> str:
        lines = ["# Demo Report", ""]
        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append(section.body)
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def build_report(
    snapshot: Dict[str, Any],
    metrics: MetricsRegistry,
    traces: TraceRecorder,
    decisions: List[PolicyDecision],
) -> DemoReport:
    sections: List[ReportSection] = []
    plugin_manager = PluginManager()
    plugin_manager.register(InventoryAlertPlugin())
    plugin_manager.register(OrderSummaryPlugin())
    plugin_results = plugin_manager.run_all(snapshot)

    metrics_summary = metrics.summary()
    sections.append(
        ReportSection(
            title="Metrics",
            body=json.dumps(metrics_summary, indent=2, sort_keys=True),
        )
    )
    sections.append(
        ReportSection(
            title="Policy Decisions",
            body="\n".join(f"- {d.reason} ({d.risk})" for d in decisions) or "None",
        )
    )
    sections.append(
        ReportSection(
            title="Plugin Results",
            body=json.dumps([r.__dict__ for r in plugin_results], indent=2, sort_keys=True),
        )
    )
    sections.append(
        ReportSection(
            title="Trace Preview",
            body=traces.export_markdown(),
        )
    )
    return DemoReport(sections=sections)
