import os

from supply_chain_demo.client import GatewayClient


def test_client_flow():
    client = GatewayClient(os.environ["GATEWAY_URL"])
    assert client.health()["status"] == "ok"
    user = client.create_user("Demo", "demo@example.com")
    order = client.create_order(user["id"], "starter-kit", 1)
    inventory = client.list_inventory()
    assert order["id"]
    assert any(item["sku"] == "starter-kit" for item in inventory)


def test_client_report():
    client = GatewayClient(os.environ["GATEWAY_URL"])
    report = client.report()
    assert "report" in report
