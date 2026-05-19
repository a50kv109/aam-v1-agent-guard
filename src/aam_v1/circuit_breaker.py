"""
Circuit Breaker with Hysteresis for AAM-V1
"""

from enum import Enum
from typing import Optional
from datetime import datetime


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Hard interrupt active
    HALF_OPEN = "half_open"  # Recovery mode


class CircuitBreaker:
    """
    Hysteresis-based circuit breaker for intervention logic.
    
    Implements 3/5 hysteresis:
    - Need 3 consecutive critical signals to OPEN
    - Need 5 consecutive nominal signals to CLOSE
    """
    
    def __init__(self, 
                 critical_threshold: int = 3,
                 recovery_threshold: int = 5,
                 recovery_budget: int = 3):
        """
        Initialize circuit breaker.
        
        Args:
            critical_threshold: Steps before opening (criticality confirmation)
            recovery_threshold: Steps before closing (recovery confirmation)
            recovery_budget: Max times we can open per session
        """
        self.critical_threshold = critical_threshold
        self.recovery_threshold = recovery_threshold
        self.recovery_budget = recovery_budget
        
        self.state = CircuitState.CLOSED
        self.critical_streak = 0
        self.nominal_streak = 0
        self.open_count = 0
        self.last_change = datetime.now()
    
    def signal(self, is_critical: bool) -> bool:
        """
        Signal criticality. Returns whether to INTERRUPT.
        
        Args:
            is_critical: Whether current signal indicates criticality
        
        Returns:
            True if we should INTERRUPT, False otherwise
        """
        
        if is_critical:
            self.nominal_streak = 0
            self.critical_streak += 1
        else:
            self.critical_streak = 0
            self.nominal_streak += 1
        
        # Transition logic
        if self.state == CircuitState.CLOSED:
            if self.critical_streak >= self.critical_threshold:
                if self.recovery_budget > 0:
                    self._open()
                    return True
        
        elif self.state == CircuitState.OPEN:
            if self.nominal_streak >= self.recovery_threshold:
                self._half_open()
        
        elif self.state == CircuitState.HALF_OPEN:
            if self.critical_streak >= 1:
                self._open()
                return True
            elif self.nominal_streak >= self.recovery_threshold:
                self._close()
        
        return False
    
    def _open(self) -> None:
        """Transition to OPEN state."""
        self.state = CircuitState.OPEN
        self.recovery_budget -= 1
        self.open_count += 1
        self.critical_streak = 0
        self.nominal_streak = 0
        self.last_change = datetime.now()
    
    def _half_open(self) -> None:
        """Transition to HALF_OPEN state."""
        self.state = CircuitState.HALF_OPEN
        self.critical_streak = 0
        self.nominal_streak = 0
        self.last_change = datetime.now()
    
    def _close(self) -> None:
        """Transition to CLOSED state."""
        self.state = CircuitState.CLOSED
        self.critical_streak = 0
        self.nominal_streak = 0
        self.last_change = datetime.now()
    
    def get_state(self) -> dict:
        """Get current circuit breaker state."""
        return {
            "state": self.state.value,
            "critical_streak": self.critical_streak,
            "nominal_streak": self.nominal_streak,
            "open_count": self.open_count,
            "recovery_budget": self.recovery_budget,
            "last_change": self.last_change.isoformat()
        }
    
    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        self.state = CircuitState.CLOSED
        self.critical_streak = 0
        self.nominal_streak = 0
        self.open_count = 0
        self.recovery_budget = 3
        self.last_change = datetime.now()
