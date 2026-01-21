from supply_chain_demo.policy import PolicyEngine
from supply_chain_demo.simulator import run_simulation


def test_simulation_produces_snapshot():
    policy = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit", "pro-kit"], enforce=True)
    result = run_simulation(policy, seed=3)
    assert "inventory" in result.snapshot
    assert result.decisions
    assert any(user["email"] == "demo@example.com" for user in result.snapshot["users"])
