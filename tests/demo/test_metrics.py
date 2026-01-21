from supply_chain_demo.metrics import MetricsRegistry


def test_metrics_record_and_summary():
    registry = MetricsRegistry()
    registry.record("http_get", 0.1)
    registry.record("http_get", 0.2)
    summary = registry.summary()
    assert summary["http_get"]["count"] == 2
    assert summary["http_get"]["avg"] > 0


def test_metrics_merge():
    left = MetricsRegistry()
    right = MetricsRegistry()
    left.record("http_get", 0.1)
    right.record("http_get", 0.2)
    left.merge(right)
    summary = left.summary()
    assert summary["http_get"]["count"] == 2


def test_metrics_iter():
    registry = MetricsRegistry()
    registry.record("http_get", 0.1)
    assert list(registry.iter_metrics()) == ["http_get"]
