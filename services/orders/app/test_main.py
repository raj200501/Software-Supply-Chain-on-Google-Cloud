from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_create_order() -> None:
    response = client.post(
        "/orders",
        json={"user_id": "user-1", "item_id": "item-1", "total": 10.0},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "order-1"
