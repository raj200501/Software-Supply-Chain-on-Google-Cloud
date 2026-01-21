import io
import json
import os

from supply_chain_demo.logging import StructuredLogger


def test_logger_text_output():
    stream = io.StringIO()
    logger = StructuredLogger("demo", stream=stream)
    logger.info("hello", key="value")
    output = stream.getvalue()
    assert "hello" in output
    assert "key=value" in output


def test_logger_json_output():
    stream = io.StringIO()
    os.environ["LOG_FORMAT"] = "json"
    logger = StructuredLogger("demo", stream=stream)
    logger.info("hello", key="value")
    payload = json.loads(stream.getvalue())
    assert payload["message"] == "hello"
    assert payload["key"] == "value"
    os.environ.pop("LOG_FORMAT", None)
