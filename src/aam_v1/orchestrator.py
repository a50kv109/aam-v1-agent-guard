"""AgentManagerOrchestrator - Main rabbit hole prevention engine.

Author: Andrey A. Artsybashev
Version: 1.0
DOI: 10.5281/zenodo.20214580
"""

import numpy as np
from collections import deque
from typing import Dict, Any, Optional, Tuple
import time


class AgentManagerOrchestrator:
    """
    Production-ready Rabbit Hole Prevention Engine (AAM-V1).
    
    Detects trajectory collapse in LLM agents via topological analysis
    of latent space dynamics. Lightweight, numerically stable, cold-start protected.
    
    Attributes:
        window_size: Rolling window for embedding history
        recovery_budget: Max hard interrupts per session
        pr_threshold: Participation ratio threshold
        mobility_threshold: Centroid mobility threshold
        enr_threshold: Evidence novelty ratio threshold
    """
    
    def __init__(self, 
                 window_size: int = 8,
                 recovery_budget: int = 3,
                 pr_threshold: float = 0.32,
                 mobility_threshold: float = 0.09,
                 enr_threshold: float = 0.07,
                 proj_dim: int = 64):
        """
        Initialize orchestrator with configurable thresholds.
        
        Args:
            window_size: Size of rolling embedding buffer
            recovery_budget: Number of allowed hard interrupts
            pr_threshold: Participation ratio threshold (collapse detection)
            mobility_threshold: Centroid mobility threshold
            enr_threshold: Evidence novelty ratio threshold
            proj_dim: Dimension for Johnson-Lindenstrauss projection
        """
        self.window_size = window_size
        self.recovery_budget = recovery_budget
        self.initial_recovery_budget = recovery_budget
        self.pr_threshold = pr_threshold
        self.mobility_threshold = mobility_threshold
        self.enr_threshold = enr_threshold
        
        # Buffers
        self.embedding_window = deque(maxlen=window_size)
        self.tools_history = deque(maxlen=16)
        self.critical_streak = 0
        self.allow_streak = 0
        self.total_pressure = 1.0
        self.evidence_bytes = 0
        
        # Projection matrix for Johnson-Lindenstrauss
        self.proj_dim = proj_dim
        self.proj_matrix: Optional[np.ndarray] = None
        
        # Constants
        self.EPS = 1e-9
        self.CONFIRMATION_CYCLES = 3
        self.RECOVERY_CYCLES = 5
        
        # Metrics history
        self.metrics_history: Dict[str, list] = {
            'pr': [],
            'mobility': [],
            'enr': [],
            'tes': [],
            'cei': []
        }

    def _get_projection_matrix(self, input_dim: int) -> np.ndarray:
        """Get or create Johnson-Lindenstrauss projection matrix.
        
        Args:
            input_dim: Input embedding dimension
            
        Returns:
            Projection matrix of shape (input_dim, proj_dim)
        """
        if self.proj_matrix is None or self.proj_matrix.shape[0] != input_dim:
            rng = np.random.default_rng(42)  # reproducible
            self.proj_matrix = rng.normal(size=(input_dim, self.proj_dim)).astype(np.float32)
            self.proj_matrix /= np.sqrt(self.proj_dim)
        return self.proj_matrix

    def _project(self, embedding: np.ndarray) -> np.ndarray:
        """Apply Johnson-Lindenstrauss random projection.
        
        Args:
            embedding: Input embedding vector
            
        Returns:
            Projected embedding of dimension proj_dim
        """
        proj = self._get_projection_matrix(embedding.shape[0])
        return embedding @ proj

    def add_step(self, 
                 thought_embedding: np.ndarray,
                 tool_name: str,
                 new_evidence_tokens: int,
                 verification_score: float = 1.0) -> Dict[str, Any]:
        """
        Process agent step and check for trajectory collapse.
        
        Main entry point. Call before/after each agent step.
        
        Args:
            thought_embedding: Hidden state or embedding from model (shape: (embedding_dim,))
            tool_name: Name of tool being used
            new_evidence_tokens: Number of new tokens in context
            verification_score: Progress score (0.0 to 1.0)
            
        Returns:
            Decision dictionary with status and metrics:
            {
                'status': 'COLD_START' | 'NOMINAL' | 'HARD_INTERRUPT' | 'ESCALATE',
                'metrics': {...},
                'action': str,  # if HARD_INTERRUPT
                'message': str
            }
        """
        # Project and store
        proj_emb = self._project(thought_embedding)
        self.embedding_window.append(proj_emb)
        self.tools_history.append(tool_name)
        
        # Update evidence tracking
        self.evidence_bytes += new_evidence_tokens
        self.total_pressure += new_evidence_tokens + 8

        # Cold start protection
        if len(self.embedding_window) < self.window_size:
            return {"status": "COLD_START", "allow": True}

        # Compute all metrics
        pr = self._compute_participation_ratio()
        mobility = self._compute_mobility()
        enr = self.evidence_bytes / (self.total_pressure + self.EPS)
        tes = self._compute_tes()
        cei = self._compute_cei(enr)
        
        # Store metrics history
        self.metrics_history['pr'].append(pr)
        self.metrics_history['mobility'].append(mobility)
        self.metrics_history['enr'].append(enr)
        self.metrics_history['tes'].append(tes)
        self.metrics_history['cei'].append(cei)

        # Detect critical state (multi-metric convergence)
        is_critical = (
            (pr < self.pr_threshold and mobility < self.mobility_threshold and enr < self.enr_threshold) or
            (tes < 0.28 and len(self.tools_history) > 5) or
            (cei < 0.18) or
            (verification_score < 0.45 and len(self.tools_history) > 6)
        )

        # Hysteresis: confirmation + reset logic
        if is_critical:
            self.critical_streak += 1
            self.allow_streak = 0
            
            if self.critical_streak >= self.CONFIRMATION_CYCLES:
                if self.recovery_budget > 0:
                    self.recovery_budget -= 1
                    self.critical_streak = 0  # Reset streak after intervention
                    return {
                        "status": "HARD_INTERRUPT",
                        "action": "ORTHOGONAL_RESET",
                        "message": "Trajectory collapse detected. Resetting hypotheses and forcing environment grounding.",
                        "metrics": {"PR": float(pr), "Mobility": float(mobility), "ENR": float(enr), "TES": float(tes), "CEI": float(cei)},
                        "recovery_remaining": self.recovery_budget
                    }
                else:
                    return {
                        "status": "ESCALATE", 
                        "reason": "Recovery budget exhausted",
                        "metrics": {"PR": float(pr), "Mobility": float(mobility), "ENR": float(enr), "TES": float(tes), "CEI": float(cei)}
                    }
        else:
            self.allow_streak += 1
            self.critical_streak = 0

        return {
            "status": "NOMINAL",
            "metrics": {"PR": float(pr), "Mobility": float(mobility), "ENR": float(enr), "TES": float(tes), "CEI": float(cei)}
        }

    def _compute_participation_ratio(self) -> float:
        """Compute Participation Ratio via eigenvalues of covariance matrix.
        
        Detects topological dimensionality collapse.
        
        Returns:
            Participation ratio (0 to 1, higher = more distributed)
        """
        data = np.stack(self.embedding_window, axis=0)
        cov = np.cov(data.T)
        
        # Handle 1D case
        if cov.ndim == 0:
            return 1.0
        
        eigenvalues = np.abs(np.linalg.eigvalsh(cov))
        eigenvalues = eigenvalues[eigenvalues > self.EPS]
        
        if len(eigenvalues) == 0:
            return 0.0
            
        sum_eig = np.sum(eigenvalues)
        return float((sum_eig ** 2) / (np.sum(eigenvalues ** 2) + self.EPS))

    def _compute_mobility(self) -> float:
        """Compute centroid mobility in projected space.
        
        Detects stagnation via Euclidean distance between consecutive centroids.
        
        Returns:
            Mobility score (higher = more movement)
        """
        if len(self.embedding_window) < 2:
            return 1.0
        
        data = np.stack(list(self.embedding_window), axis=0)
        
        # Split into two halves
        mid = len(data) // 2
        c_prev = np.mean(data[:mid], axis=0)
        c_curr = np.mean(data[mid:], axis=0)
        
        return float(np.linalg.norm(c_curr - c_prev) + self.EPS)

    def _compute_tes(self) -> float:
        """Compute Tool Effectiveness Score (Write/Read asymmetry).
        
        Detects overuse of read-only tools (symptom of looping).
        
        Returns:
            TES score (0 to 1, higher = more write tools)
        """
        recent = list(self.tools_history)[-12:]
        
        # Define write tools (customize per environment)
        write_tools = {
            "file_editor", "code_execution", "bash_write", 
            "git_commit", "reasoning_step", "memory_write"
        }
        
        write_count = sum(1 for t in recent if t in write_tools)
        return float(write_count / max(len(recent), 1))
    
    def _compute_cei(self, enr: float) -> float:
        """Compute Context Entropy Index.
        
        Combines tool diversity with evidence novelty.
        
        Args:
            enr: Evidence novelty ratio
            
        Returns:
            CEI score
        """
        unique_tools = len(set(self.tools_history))
        total_tools = len(self.tools_history)
        
        if total_tools == 0:
            return 0.0
        
        diversity = unique_tools / total_tools
        return float(diversity * (1.0 - enr))

    def reset(self) -> None:
        """Reset orchestrator state (after hard interrupt)."""
        self.embedding_window.clear()
        self.tools_history.clear()
        self.critical_streak = 0
        self.allow_streak = 0
        self.total_pressure = 1.0
        self.evidence_bytes = 0

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of recent metrics.
        
        Returns:
            Dictionary with metric statistics
        """
        if not self.metrics_history['pr']:
            return {}
        
        return {
            'pr': {
                'current': self.metrics_history['pr'][-1] if self.metrics_history['pr'] else None,
                'mean': float(np.mean(self.metrics_history['pr'])),
                'std': float(np.std(self.metrics_history['pr']))
            },
            'mobility': {
                'current': self.metrics_history['mobility'][-1] if self.metrics_history['mobility'] else None,
                'mean': float(np.mean(self.metrics_history['mobility'])),
                'std': float(np.std(self.metrics_history['mobility']))
            },
            'recovery_budget_remaining': self.recovery_budget,
            'interrupts_used': self.initial_recovery_budget - self.recovery_budget
        }
