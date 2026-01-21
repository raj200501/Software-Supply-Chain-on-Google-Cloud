"""Simulation helpers for repeatable demo runs."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List

from .policy import PolicyEngine, PolicyDecision


@dataclass
class SimulationResult:
    snapshot: Dict[str, Any]
    decisions: List[PolicyDecision]


def run_simulation(policy: PolicyEngine, seed: int = 7) -> SimulationResult:
    rng = random.Random(seed)
    decisions: List[PolicyDecision] = []
    users = []
    for idx in range(3):
        email = "demo@example.com" if idx == 0 else f"user{idx}@example.com"
        decision = policy.evaluate_user(email)
        decisions.append(decision)
        if decision.allowed:
            users.append({"id": f"user-{idx}", "email": email})
    orders = []
    inventory = {"starter-kit": 3, "pro-kit": 2}
    for idx in range(5):
        sku = rng.choice(list(inventory.keys()))
        quantity = rng.randint(1, 2)
        decision = policy.evaluate_order(sku, quantity)
        decisions.append(decision)
        if decision.allowed:
            inventory[sku] -= quantity
            orders.append({"id": f"order-{idx}", "sku": sku, "quantity": quantity})
    decisions.append(policy.evaluate_inventory_snapshot(inventory))
    snapshot = {
        "users": users,
        "orders": orders,
        "inventory": inventory,
    }
    return SimulationResult(snapshot=snapshot, decisions=decisions)
