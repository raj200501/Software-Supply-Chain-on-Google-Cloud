"""Supply chain demo toolkit used for local verification and demos."""

from .gateway import GatewayServer, GatewayConfig
from .policy import PolicyDecision, PolicyEngine, RiskLevel
from .trace import TraceRecorder, TraceEvent
from .metrics import MetricsRegistry, Timer
from .logging import StructuredLogger
from .storage import SnapshotStore
from .plugins import PluginManager, PluginResult, InventoryAlertPlugin, OrderSummaryPlugin
from .report import DemoReport, build_report
from .simulator import SimulationResult, run_simulation
from .doctor import Diagnostic, run_diagnostics

__all__ = [
    "GatewayServer",
    "GatewayConfig",
    "PolicyDecision",
    "PolicyEngine",
    "RiskLevel",
    "TraceRecorder",
    "TraceEvent",
    "MetricsRegistry",
    "Timer",
    "StructuredLogger",
    "SnapshotStore",
    "PluginManager",
    "PluginResult",
    "InventoryAlertPlugin",
    "OrderSummaryPlugin",
    "DemoReport",
    "build_report",
    "SimulationResult",
    "run_simulation",
    "Diagnostic",
    "run_diagnostics",
]
