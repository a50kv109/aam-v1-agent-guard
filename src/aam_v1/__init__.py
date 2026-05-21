"""
AAM-V1: Operational Physiology for Autonomous Agents
Runtime Collapse Detection & Survivability Monitoring

Core Module Exports
"""

__version__ = "0.9.0"  # Research transition phase - NOT production
__author__ = "Andrey A. Artsybashev"
__canonical_id__ = "AAM-V1_ARTSYBASHEV_UA_KHARKIV_AIANALYSIS"
__doi__ = "10.5281/zenodo.20214580"
__license__ = "MIT"

# Phase indicator
RESEARCH_PHASE = True
PRODUCTION_READY = False

from .orchestrator import AgentManagerOrchestrator
from .metrics import MetricEngine
from .circuit_breaker import CircuitBreaker, CircuitState

__all__ = [
    "AgentManagerOrchestrator",
    "MetricEngine",
    "CircuitBreaker",
    "CircuitState",
]

# Default research parameters (not validated for production use)
DEFAULT_PR_THRESHOLD = 0.32          # Participation Ratio collapse
DEFAULT_MOBILITY_THRESHOLD = 0.09    # Stagnation detection
DEFAULT_ENR_THRESHOLD = 0.07         # Evidence starvation
DEFAULT_WINDOW_SIZE = 8              # Embedding history window
DEFAULT_RECOVERY_BUDGET = 3          # Hard interrupts per session
