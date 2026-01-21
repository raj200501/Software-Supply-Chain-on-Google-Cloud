from supply_chain_demo.diff import diff_snapshots


def test_diff_detects_changes():
    before = {"users": 1, "orders": 0}
    after = {"users": 2, "orders": 0, "inventory": 5}
    diff = diff_snapshots(before, after)
    assert "inventory" in diff.added
    assert "users" in diff.changed
    assert diff.removed == {}
