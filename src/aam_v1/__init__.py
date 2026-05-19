"""
AAM-V1: Topological Telemetry and Evidence-Based Runtime for Long-Horizon Autonomous Agents

Author: Andrey A. Artsybashev (Kharkiv, Ukraine)
Version: 1.0
License: MIT
DOI: 10.5281/zenodo.20214580
"""

__version__ = "1.0.0"
__author__ = "Andrey A. Artsybashev"
__canonical_id__ = "AAM-V1_ARTSYBASHEV_UA_KHARKIV_AIANALYSIS"
__doi__ = "10.5281/zenodo.20214580"

from .orchestrator import AgentManagerOrchestrator
from .metrics import MetricEngine
from .circuit_breaker import CircuitBreaker

__all__ = [
    "AgentManagerOrchestrator",
    "MetricEngine",
    "CircuitBreaker",
]
