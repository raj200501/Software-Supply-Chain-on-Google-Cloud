from supply_chain_demo.metrics import MetricsRegistry
from supply_chain_demo.policy import PolicyDecision, RiskLevel
from supply_chain_demo.report import build_report
from supply_chain_demo.trace import TraceRecorder


def test_report_contains_sections():
    snapshot = {"inventory": {"starter-kit": 1}, "orders": []}
    metrics = MetricsRegistry()
    metrics.record("http_get", 0.1)
    tracer = TraceRecorder(enabled=False)
    tracer.record("event", foo="bar")
    decisions = [PolicyDecision(True, "ok", RiskLevel.LOW)]
    report = build_report(snapshot, metrics, tracer, decisions)
    markdown = report.as_markdown()
    assert "Metrics" in markdown
    assert "Policy Decisions" in markdown
    assert "Trace Report" in markdown
