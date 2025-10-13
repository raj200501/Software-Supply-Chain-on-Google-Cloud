from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="orders-service")


class OrderIn(BaseModel):
    user_id: str
    item_id: str
    total: float


class OrderOut(BaseModel):
    id: str
    user_id: str
    item_id: str
    total: float


@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderIn) -> OrderOut:
    return OrderOut(id="order-1", **order.dict())
