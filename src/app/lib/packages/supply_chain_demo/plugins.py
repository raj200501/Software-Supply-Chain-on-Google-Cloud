"""Plugin architecture for demo analytics."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Protocol, Tuple


@dataclass
class PluginResult:
    name: str
    ok: bool
    summary: str
    details: Dict[str, Any]


class Plugin(Protocol):
    name: str

    def describe(self) -> str: ...

    def run(self, snapshot: Dict[str, Any]) -> PluginResult: ...


class PluginManager:
    """Loads and runs plugins from built-in or dotted-path modules."""

    def __init__(self) -> None:
        self._plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        self._plugins[plugin.name] = plugin

    def load_from_module(self, module_path: str, symbol: str) -> None:
        module = importlib.import_module(module_path)
        plugin = getattr(module, symbol)
        self.register(plugin())

    def run_all(self, snapshot: Dict[str, Any]) -> List[PluginResult]:
        results = []
        for plugin in self._plugins.values():
            results.append(plugin.run(snapshot))
        return results

    def describe_all(self) -> List[Tuple[str, str]]:
        return [(plugin.name, plugin.describe()) for plugin in self._plugins.values()]


class InventoryAlertPlugin:
    name = "inventory_alert"

    def describe(self) -> str:
        return "Flags low inventory items"

    def run(self, snapshot: Dict[str, Any]) -> PluginResult:
        inventory = snapshot.get("inventory", {})
        low = {sku: qty for sku, qty in inventory.items() if qty <= 1}
        ok = len(low) == 0
        summary = "inventory healthy" if ok else "low inventory detected"
        return PluginResult(
            name=self.name,
            ok=ok,
            summary=summary,
            details={"low": low},
        )


class OrderSummaryPlugin:
    name = "order_summary"

    def describe(self) -> str:
        return "Summarizes order counts by sku"

    def run(self, snapshot: Dict[str, Any]) -> PluginResult:
        orders = snapshot.get("orders", [])
        summary: Dict[str, int] = {}
        for order in orders:
            sku = order.get("sku")
            summary[sku] = summary.get(sku, 0) + int(order.get("quantity", 0))
        return PluginResult(
            name=self.name,
            ok=True,
            summary="order summary computed",
            details={"totals": summary},
        )
