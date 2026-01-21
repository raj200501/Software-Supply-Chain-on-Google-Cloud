from supply_chain_demo.plugins import PluginManager, InventoryAlertPlugin, OrderSummaryPlugin


def test_plugin_manager_runs_plugins():
    manager = PluginManager()
    manager.register(InventoryAlertPlugin())
    manager.register(OrderSummaryPlugin())
    snapshot = {"inventory": {"starter-kit": 0}, "orders": [{"sku": "starter-kit", "quantity": 1}]}
    results = manager.run_all(snapshot)
    names = {result.name for result in results}
    assert "inventory_alert" in names
    assert "order_summary" in names


def test_inventory_alert_plugin_flags_low():
    plugin = InventoryAlertPlugin()
    result = plugin.run({"inventory": {"starter-kit": 0}})
    assert not result.ok
    assert "starter-kit" in result.details["low"]


def test_order_summary_plugin_counts_orders():
    plugin = OrderSummaryPlugin()
    result = plugin.run({"orders": [{"sku": "starter-kit", "quantity": 2}]})
    assert result.details["totals"]["starter-kit"] == 2
