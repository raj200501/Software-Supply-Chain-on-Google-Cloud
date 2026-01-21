import json
import os
import tempfile

from supply_chain_demo.trace import TraceRecorder


def test_trace_records_events_in_memory():
    recorder = TraceRecorder(enabled=False)
    recorder.record("event_one", foo="bar")
    recorder.record("event_two", count=2)
    events = recorder.events()
    assert len(events) == 2
    assert events[0].name == "event_one"


def test_trace_writes_jsonl_when_enabled():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "trace.jsonl")
        recorder = TraceRecorder(path=path, enabled=True)
        recorder.record("event_one", foo="bar")
        recorder.record("event_two", count=2)
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
        assert len(lines) == 2
        payload = json.loads(lines[0])
        assert payload["name"] == "event_one"
        assert payload["attributes"]["foo"] == "bar"


def test_trace_exports_markdown():
    recorder = TraceRecorder(enabled=False)
    recorder.record("event_one", foo="bar")
    md = recorder.export_markdown()
    assert "Trace Report" in md
    assert "event_one" in md
