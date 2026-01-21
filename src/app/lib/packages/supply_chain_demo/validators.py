"""Input validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ValidationResult:
    ok: bool
    message: str


def validate_user_payload(payload: Dict[str, str]) -> ValidationResult:
    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    if not name:
        return ValidationResult(False, "name is required")
    if "@" not in email:
        return ValidationResult(False, "email is invalid")
    return ValidationResult(True, "ok")


def validate_order_payload(payload: Dict[str, str]) -> ValidationResult:
    sku = payload.get("item", "").strip()
    quantity = payload.get("quantity")
    if not sku:
        return ValidationResult(False, "item is required")
    try:
        qty = int(quantity)
    except (TypeError, ValueError):
        return ValidationResult(False, "quantity must be an integer")
    if qty <= 0:
        return ValidationResult(False, "quantity must be positive")
    return ValidationResult(True, "ok")
