"""Scenario library for deterministic demos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .policy import PolicyDecision, PolicyEngine


@dataclass
class ScenarioStep:
    name: str
    payload: Dict[str, Any]


@dataclass
class ScenarioResult:
    name: str
    decisions: List[PolicyDecision]
    events: List[str]


class DemoScenario:
    """Defines a deterministic scenario and evaluates it with policy."""

    def __init__(self, name: str, steps: List[ScenarioStep]) -> None:
        self.name = name
        self.steps = steps

    def run(self, policy: PolicyEngine) -> ScenarioResult:
        decisions: List[PolicyDecision] = []
        events: List[str] = []
        for step in self.steps:
            if step.name == "user":
                decision = policy.evaluate_user(step.payload["email"])
                decisions.append(decision)
                events.append(f"user:{step.payload['email']}")
            elif step.name == "order":
                decision = policy.evaluate_order(step.payload["sku"], int(step.payload["quantity"]))
                decisions.append(decision)
                events.append(f"order:{step.payload['sku']}")
            elif step.name == "inventory":
                decision = policy.evaluate_inventory_snapshot(step.payload["inventory"])
                decisions.append(decision)
                events.append("inventory-check")
        return ScenarioResult(name=self.name, decisions=decisions, events=events)


def default_scenario() -> DemoScenario:
    steps = [
        ScenarioStep(name="user", payload={"email": "demo@example.com"}),
        ScenarioStep(name="order", payload={"sku": "starter-kit", "quantity": 1}),
        ScenarioStep(name="inventory", payload={"inventory": {"starter-kit": 2}}),
    ]
    return DemoScenario(name="default", steps=steps)
