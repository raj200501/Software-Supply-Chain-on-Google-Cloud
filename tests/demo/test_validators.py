from supply_chain_demo.validators import validate_user_payload, validate_order_payload


def test_validate_user_requires_name():
    result = validate_user_payload({"name": "", "email": "demo@example.com"})
    assert not result.ok


def test_validate_user_requires_email():
    result = validate_user_payload({"name": "Demo", "email": "invalid"})
    assert not result.ok


def test_validate_order_requires_sku():
    result = validate_order_payload({"item": "", "quantity": 1})
    assert not result.ok


def test_validate_order_quantity_positive():
    result = validate_order_payload({"item": "starter-kit", "quantity": 0})
    assert not result.ok


def test_validate_order_ok():
    result = validate_order_payload({"item": "starter-kit", "quantity": 1})
    assert result.ok
