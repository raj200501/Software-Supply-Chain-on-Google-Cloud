from supply_chain_demo.workflow import OrderRecord, OrderState, OrderWorkflow


def test_workflow_completes_order():
    inventory = {"starter-kit": 2}
    order = OrderRecord(order_id="1", sku="starter-kit", quantity=1)
    workflow = OrderWorkflow()
    result = workflow.run(order, inventory)
    assert result.state == OrderState.COMPLETED
    assert inventory["starter-kit"] == 1


def test_workflow_fails_when_insufficient_inventory():
    inventory = {"starter-kit": 0}
    order = OrderRecord(order_id="1", sku="starter-kit", quantity=1)
    workflow = OrderWorkflow()
    result = workflow.run(order, inventory)
    assert result.state == OrderState.FAILED
