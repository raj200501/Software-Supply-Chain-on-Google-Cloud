from supply_chain_demo.policy import PolicyEngine, RiskLevel


def test_policy_disabled_allows_user():
    engine = PolicyEngine(allowed_users=["a"], allowed_skus=["starter-kit"], enforce=False)
    decision = engine.evaluate_user("unknown@example.com")
    assert decision.allowed
    assert decision.risk == RiskLevel.LOW


def test_policy_blocks_unknown_user_when_enabled():
    engine = PolicyEngine(allowed_users=["a"], allowed_skus=["starter-kit"], enforce=True)
    decision = engine.evaluate_user("unknown@example.com")
    assert not decision.allowed
    assert decision.risk == RiskLevel.MEDIUM


def test_policy_allows_known_user_when_enabled():
    engine = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit"], enforce=True)
    decision = engine.evaluate_user("demo@example.com")
    assert decision.allowed


def test_policy_rejects_unknown_sku():
    engine = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit"], enforce=True)
    decision = engine.evaluate_order("unknown", 1)
    assert not decision.allowed
    assert decision.risk == RiskLevel.HIGH


def test_policy_rejects_large_quantity():
    engine = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit"], enforce=True, max_quantity=1)
    decision = engine.evaluate_order("starter-kit", 2)
    assert not decision.allowed
    assert decision.risk == RiskLevel.MEDIUM


def test_policy_inventory_negative():
    engine = PolicyEngine(allowed_users=["demo@example.com"], allowed_skus=["starter-kit"], enforce=True)
    decision = engine.evaluate_inventory_snapshot({"starter-kit": -1})
    assert not decision.allowed
    assert decision.risk == RiskLevel.HIGH
