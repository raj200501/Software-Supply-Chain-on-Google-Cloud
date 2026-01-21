from supply_chain_demo.policy import PolicyEngine
from supply_chain_demo.scenarios import default_scenario


def test_default_scenario_runs():
    policy = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit"], enforce=True)
    scenario = default_scenario()
    result = scenario.run(policy)
    assert result.name == "default"
    assert len(result.decisions) == 3
    assert "order:starter-kit" in result.events
