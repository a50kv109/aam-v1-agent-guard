"""
AgentManagerOrchestrator - Main orchestration class for AAM-V1
Lightweight rabbit hole prevention engine with hysteresis and recovery budget
"""

import numpy as np
from collections import deque
from typing import Dict, Any, Optional
import time


class AgentManagerOrchestrator:
    """
    Production-ready Rabbit Hole Prevention Engine (AAM-V1).
    Lightweight, numerically stable, cold-start protected.
    
    Uses topological analysis (PR + Mobility) combined with
    evidence-based metrics (ENR, TES, CEI) to detect trajectory collapse.
    """
    
    def __init__(self, 
                 window_size: int = 8,
                 recovery_budget: int = 3,
                 pr_threshold: float = 0.32,
                 mobility_threshold: float = 0.09,
                 enr_threshold: float = 0.07):
        """
        Initialize AgentManagerOrchestrator.
        
        Args:
            window_size: Size of rolling embedding window
            recovery_budget: Max hard interrupts per session
            pr_threshold: Participation Ratio detection threshold
            mobility_threshold: Mobility detection threshold
            enr_threshold: Evidence Novelty Ratio threshold
        """
        
        self.window_size = window_size
        self.recovery_budget = recovery_budget
        self.pr_threshold = pr_threshold
        self.mobility_threshold = mobility_threshold
        self.enr_threshold = enr_threshold
        
        # Buffers
        self.embedding_window = deque(maxlen=window_size)
        self.tools_history = deque(maxlen=16)
        
        # State tracking
        self.critical_streak = 0
        self.allow_streak = 0
        self.total_pressure = 1.0
        self.evidence_bytes = 0
        
        # Projection matrix for Johnson-Lindenstrauss
        self.proj_dim = 64
        self.proj_matrix: Optional[np.ndarray] = None
        
        # Constants
        self.EPS = 1e-9
        self.CONFIRMATION_CYCLES = 3
        self.RECOVERY_CYCLES = 5

    def _get_projection_matrix(self, input_dim: int) -> np.ndarray:
        """Get or initialize Johnson-Lindenstrauss projection matrix."""
        if self.proj_matrix is None or self.proj_matrix.shape[0] != input_dim:
            rng = np.random.default_rng(42)  # reproducible
            self.proj_matrix = rng.normal(size=(input_dim, self.proj_dim)).astype(np.float32)
            self.proj_matrix /= np.sqrt(self.proj_dim)
        return self.proj_matrix

    def _project(self, embedding: np.ndarray) -> np.ndarray:
        """Apply Johnson-Lindenstrauss Random Projection."""
        proj = self._get_projection_matrix(embedding.shape[0])
        return embedding @ proj

    def add_step(self, 
                 thought_embedding: np.ndarray,
                 tool_name: str,
                 new_evidence_tokens: int,
                 verification_score: float = 1.0) -> Dict[str, Any]:
        """
        Main entry point. Call before/after each agent step.
        
        Args:
            thought_embedding: Current thought embedding from model (any dimension)
            tool_name: Name of tool being invoked
            new_evidence_tokens: Number of new evidence tokens acquired
            verification_score: Score indicating progress (0.0 to 1.0)
        
        Returns:
            Decision dict with status, metrics, and optional intervention action
        """
        
        # Ensure embedding is float32 numpy array
        if not isinstance(thought_embedding, np.ndarray):
            thought_embedding = np.array(thought_embedding, dtype=np.float32)
        else:
            thought_embedding = thought_embedding.astype(np.float32)
        
        # Project and store
        proj_emb = self._project(thought_embedding)
        self.embedding_window.append(proj_emb)
        self.tools_history.append(tool_name)
        
        # Update evidence tracking
        self.evidence_bytes += new_evidence_tokens
        self.total_pressure += new_evidence_tokens + 8

        # Cold start protection
        if len(self.embedding_window) < self.window_size:
            return {
                "status": "COLD_START",
                "allow": True,
                "message": f"Accumulating trajectory data ({len(self.embedding_window)}/{self.window_size})"
            }

        # Compute metrics
        pr = self._compute_participation_ratio()
        mobility = self._compute_mobility()
        enr = self.evidence_bytes / (self.total_pressure + self.EPS)
        tes = self._compute_tes()
        cei = self._compute_cei(enr)

        # Criticality detection
        is_critical = self._is_critical(pr, mobility, enr, tes, cei, verification_score)

        if is_critical:
            self.critical_streak += 1
            self.allow_streak = 0
            
            if self.critical_streak >= self.CONFIRMATION_CYCLES:
                if self.recovery_budget > 0:
                    self.recovery_budget -= 1
                    return {
                        "status": "HARD_INTERRUPT",
                        "action": "ORTHOGONAL_RESET",
                        "message": "Trajectory collapse detected. Resetting hypotheses and forcing environment grounding.",
                        "metrics": {
                            "PR": float(pr),
                            "Mobility": float(mobility),
                            "ENR": float(enr),
                            "TES": float(tes),
                            "CEI": float(cei)
                        },
                        "recovery_budget_remaining": self.recovery_budget
                    }
                else:
                    return {
                        "status": "ESCALATE",
                        "reason": "Recovery budget exhausted",
                        "metrics": {
                            "PR": float(pr),
                            "Mobility": float(mobility),
                            "ENR": float(enr),
                            "TES": float(tes),
                            "CEI": float(cei)
                        }
                    }
        else:
            self.allow_streak += 1
            self.critical_streak = 0

        return {
            "status": "NOMINAL",
            "metrics": {
                "PR": float(pr),
                "Mobility": float(mobility),
                "ENR": float(enr),
                "TES": float(tes),
                "CEI": float(cei)
            }
        }

    def _compute_participation_ratio(self) -> float:
        """
        Participation Ratio via eigenvalues of covariance matrix.
        Measures topological dimensionality of trajectory.
        
        PR = (sum of eigenvalues)^2 / sum of squared eigenvalues
        """
        data = np.stack(self.embedding_window)
        cov = np.cov(data.T)
        eigenvalues = np.abs(np.linalg.eigvalsh(cov))
        eigenvalues = eigenvalues[eigenvalues > self.EPS]
        
        if len(eigenvalues) == 0:
            return 0.0
            
        sum_eig = np.sum(eigenvalues)
        return float((sum_eig ** 2) / (np.sum(eigenvalues ** 2) + self.EPS))

    def _compute_mobility(self) -> float:
        """
        Euclidean distance between consecutive centroids.
        Measures displacement in low-dimensional space.
        """
        if len(self.embedding_window) < 2:
            return 1.0
        
        data = np.stack(self.embedding_window)
        c_prev = np.mean(data[-2:-1], axis=0)
        c_curr = np.mean(data[-1:], axis=0)
        return float(np.linalg.norm(c_curr - c_prev) + self.EPS)

    def _compute_tes(self) -> float:
        """
        Tool Effectiveness Score (Write/Read asymmetry).
        Detects if agent is only reading without taking action.
        """
        recent = list(self.tools_history)[-12:]
        
        # Define write tools (modify as needed for your environment)
        write_tools = {
            "file_editor", "code_execution", "bash_write", 
            "git_commit", "reasoning_step", "plan", "execute"
        }
        
        write_count = sum(1 for t in recent if t in write_tools)
        return float(write_count / max(len(recent), 1))

    def _compute_cei(self, enr: float) -> float:
        """
        Context Entropy Index.
        Measures diversity of tool usage adjusted by evidence novelty.
        """
        recent = list(self.tools_history)[-12:]
        if len(recent) == 0:
            return 0.0
        
        unique_tools = len(set(recent))
        tool_diversity = unique_tools / len(recent)
        
        return float(tool_diversity * (1.0 - enr))

    def _is_critical(self, pr: float, mobility: float, enr: float,
                     tes: float, cei: float, verification_score: float) -> bool:
        """
        Determine if trajectory is in critical state.
        Combines multiple detection heuristics.
        """
        
        # Criterion 1: Topological collapse (low PR + low Mobility + low ENR)
        topological_collapse = (
            pr < self.pr_threshold and 
            mobility < self.mobility_threshold and 
            enr < self.enr_threshold
        )
        
        # Criterion 2: Tool ineffectiveness (low TES with sufficient history)
        tool_ineffective = (
            tes < 0.28 and 
            len(self.tools_history) > 5
        )
        
        # Criterion 3: Low context entropy
        low_entropy = cei < 0.18
        
        # Criterion 4: Poor verification score with history
        poor_verification = (
            verification_score < 0.45 and 
            len(self.tools_history) > 6
        )
        
        return bool(topological_collapse or tool_ineffective or low_entropy or poor_verification)

    def reset_state(self) -> None:
        """Hard reset of internal state (call after HARD_INTERRUPT)."""
        self.embedding_window.clear()
        self.tools_history.clear()
        self.critical_streak = 0
        self.allow_streak = 0
        self.total_pressure = 1.0
        self.evidence_bytes = 0

    def get_state(self) -> Dict[str, Any]:
        """Return current orchestrator state for monitoring."""
        return {
            "window_size": len(self.embedding_window),
            "critical_streak": self.critical_streak,
            "allow_streak": self.allow_streak,
            "total_pressure": self.total_pressure,
            "evidence_bytes": self.evidence_bytes,
            "recovery_budget": self.recovery_budget,
            "tools_history_sample": list(self.tools_history)[-5:]
        }
