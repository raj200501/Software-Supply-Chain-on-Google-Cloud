import os

from supply_chain_demo.config import DemoConfig


def test_config_defaults():
    config = DemoConfig.from_env()
    assert config.host == "127.0.0.1"
    assert config.port == 8080


def test_config_env_override(monkeypatch):
    monkeypatch.setenv("DEMO_HOST", "0.0.0.0")
    monkeypatch.setenv("DEMO_PORT", "9090")
    monkeypatch.setenv("DEMO_POLICY", "1")
    monkeypatch.setenv("DEMO_TRACE", "1")
    config = DemoConfig.from_env()
    assert config.host == "0.0.0.0"
    assert config.port == 9090
    assert config.policy_enabled
    assert config.trace_enabled
