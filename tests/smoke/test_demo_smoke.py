from supply_chain_demo.demo import run_demo


def test_demo_runs():
    result = run_demo()
    assert result.ok
    assert "user_id" in result.details
    assert "order_id" in result.details
