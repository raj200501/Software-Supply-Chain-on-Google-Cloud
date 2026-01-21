"""Policy evaluation helpers for demo safety gates."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    risk: RiskLevel


@dataclass
class PolicyEngine:
    """Simple policy engine with allowlists and risk scoring."""

    allowed_users: List[str]
    allowed_skus: List[str]
    max_quantity: int = 5
    enforce: bool = False

    def evaluate_user(self, email: str) -> PolicyDecision:
        if not self.enforce:
            return PolicyDecision(True, "policy disabled", RiskLevel.LOW)
        if email in self.allowed_users:
            return PolicyDecision(True, "user allowlisted", RiskLevel.LOW)
        return PolicyDecision(False, "user not allowlisted", RiskLevel.MEDIUM)

    def evaluate_order(self, sku: str, quantity: int) -> PolicyDecision:
        if not self.enforce:
            return PolicyDecision(True, "policy disabled", RiskLevel.LOW)
        if sku not in self.allowed_skus:
            return PolicyDecision(False, "sku not allowlisted", RiskLevel.HIGH)
        if quantity > self.max_quantity:
            return PolicyDecision(False, "quantity exceeds limit", RiskLevel.MEDIUM)
        return PolicyDecision(True, "order approved", RiskLevel.LOW)

    def evaluate_inventory_snapshot(self, inventory: Dict[str, int]) -> PolicyDecision:
        if not self.enforce:
            return PolicyDecision(True, "policy disabled", RiskLevel.LOW)
        if not inventory:
            return PolicyDecision(False, "inventory empty", RiskLevel.MEDIUM)
        if any(count < 0 for count in inventory.values()):
            return PolicyDecision(False, "negative inventory", RiskLevel.HIGH)
        return PolicyDecision(True, "inventory healthy", RiskLevel.LOW)

    @classmethod
    def from_env(cls) -> "PolicyEngine":
        allowed_users = [u.strip() for u in ("demo@example.com").split(",") if u.strip()]
        allowed_skus = ["starter-kit", "pro-kit", "enterprise-kit"]
        enforce = bool(int(__import__("os").getenv("DEMO_POLICY", "0")))
        max_quantity = int(__import__("os").getenv("DEMO_POLICY_MAX_QTY", "5"))
        return cls(
            allowed_users=allowed_users,
            allowed_skus=allowed_skus,
            max_quantity=max_quantity,
            enforce=enforce,
        )
