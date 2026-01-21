"""Order workflow state machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class OrderState(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    RESERVED = "reserved"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class OrderRecord:
    order_id: str
    sku: str
    quantity: int
    state: OrderState = OrderState.CREATED
    history: List[OrderState] = field(default_factory=lambda: [OrderState.CREATED])

    def transition(self, new_state: OrderState) -> None:
        self.state = new_state
        self.history.append(new_state)


class OrderWorkflow:
    """Executes a deterministic order flow for demo purposes."""

    def validate(self, order: OrderRecord) -> None:
        if order.quantity <= 0:
            order.transition(OrderState.FAILED)
            return
        order.transition(OrderState.VALIDATED)

    def reserve(self, order: OrderRecord, inventory: Dict[str, int]) -> None:
        if order.state != OrderState.VALIDATED:
            order.transition(OrderState.FAILED)
            return
        if inventory.get(order.sku, 0) < order.quantity:
            order.transition(OrderState.FAILED)
            return
        inventory[order.sku] -= order.quantity
        order.transition(OrderState.RESERVED)

    def complete(self, order: OrderRecord) -> None:
        if order.state != OrderState.RESERVED:
            order.transition(OrderState.FAILED)
            return
        order.transition(OrderState.COMPLETED)

    def run(self, order: OrderRecord, inventory: Dict[str, int]) -> OrderRecord:
        self.validate(order)
        if order.state == OrderState.FAILED:
            return order
        self.reserve(order, inventory)
        if order.state == OrderState.FAILED:
            return order
        self.complete(order)
        return order
